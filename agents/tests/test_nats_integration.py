"""NATS integration tests for Revenue OS agent mesh — Phase B.

Tests agent-to-agent communication via a live NATS server with JetStream.
Requires a running NATS server at nats://localhost:4222 with JetStream enabled.

Start with: nats-server -js -p 4222
Run: pytest agents/tests/test_nats_integration.py -v --timeout=60
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from agent_base.event_envelope import EventEnvelope, new_event_id, new_trace_id, new_span_id
from agent_base.nats_client import NatsClient

NATS_URL = os.getenv("NATS_TEST_URL", "nats://localhost:4222")
NATS_TIMEOUT = float(os.getenv("NATS_TEST_TIMEOUT", "5"))


async def _nats_connect():
    import nats as _nats_mod
    return await _nats_mod.connect(NATS_URL)


def _from_agent(agent_dir: str, module_path: str, *names: str):
    agents_base = Path(__file__).parent.parent
    top_dir = agents_base / agent_dir
    if str(top_dir) not in sys.path:
        sys.path.insert(0, str(top_dir))
    import importlib
    mod = importlib.import_module(module_path)
    if len(names) == 1:
        return getattr(mod, names[0])
    return tuple(getattr(mod, n) for n in names)


@pytest.fixture
async def nats_raw():
    nc = await _nats_connect()
    yield nc
    await nc.drain()


@pytest.fixture
async def nats_js(nats_raw):
    yield nats_raw.jetstream()


@pytest.fixture
async def nats_client():
    client = NatsClient(servers=[NATS_URL], agent_id="test-agent-v1")
    await client.connect()
    assert client._connected
    assert not client._dev_mode
    yield client
    await client.close()


class TestNatsConnectivity:

    @pytest.mark.asyncio
    async def test_raw_connect_and_info(self, nats_raw):
        info = nats_raw._server_info
        assert info["jetstream"] is True
        assert info["port"] == 4222

    @pytest.mark.asyncio
    async def test_nats_client_wrapper_connect(self, nats_client):
        assert nats_client._connected
        assert not nats_client._dev_mode

    @pytest.mark.asyncio
    async def test_nats_client_dev_mode(self):
        dev_client = NatsClient(servers=[], agent_id="dev-agent")
        await dev_client.connect()
        assert dev_client._dev_mode
        assert dev_client._connected


class TestEventEnvelopeRoundtrip:

    @pytest.mark.asyncio
    async def test_publish_subscribe_simple(self, nats_client):
        received = []
        async def handler(msg):
            received.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub = await nc.subscribe("test.simple", cb=handler)
        await asyncio.sleep(0.3)
        envelope = EventEnvelope(event_type="TestEvent", source_agent="test-agent-v1", deal_id="d_test_001", data={"hello": "world", "number": 42})
        await nats_client.publish("test.simple", envelope)
        await asyncio.sleep(0.5)
        assert len(received) == 1
        msg = received[0]
        assert msg.event_type == "TestEvent"
        assert msg.source_agent == "test-agent-v1"
        assert msg.deal_id == "d_test_001"
        assert msg.data == {"hello": "world", "number": 42}
        assert msg.event_id.startswith("evt_")
        assert msg.trace_id.startswith("tr_")
        assert msg.spec_version == "2.0"
        await sub.unsubscribe()

    @pytest.mark.asyncio
    async def test_nats_headers_preserved(self, nats_client):
        received = []
        async def handler(msg):
            received.append(msg)
        nc = nats_client._nc
        sub = await nc.subscribe("test.headers", cb=handler)
        await asyncio.sleep(0.3)
        envelope = EventEnvelope(event_type="HeaderTest", source_agent="test-agent-v1", deal_id="d_headers_001", data={"key": "value"})
        await nats_client.publish("test.headers", envelope)
        await asyncio.sleep(0.5)
        assert len(received) == 1
        raw = received[0]
        h = raw.headers
        env = EventEnvelope.from_json(raw.data.decode())
        assert h["Nats-Msg-Id"] == env.event_id
        assert h["X-Event-Type"] == "HeaderTest"
        assert h["X-Source-Agent"] == "test-agent-v1"
        await sub.unsubscribe()

    @pytest.mark.asyncio
    async def test_trace_context_carried_through_nats(self, nats_client):
        received = []
        async def handler(msg):
            received.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub = await nc.subscribe("test.trace", cb=handler)
        await asyncio.sleep(0.3)
        trace_id = new_trace_id()
        causation_id = new_event_id()
        envelope = EventEnvelope(event_type="TraceTest", source_agent="test-agent-v1", deal_id="d_trace_001", trace_id=trace_id, causation_id=causation_id, data={"step": 1})
        await nats_client.publish("test.trace", envelope)
        await asyncio.sleep(0.5)
        assert len(received) == 1
        msg = received[0]
        assert msg.trace_id == trace_id
        assert msg.causation_id == causation_id
        await sub.unsubscribe()

    @pytest.mark.asyncio
    async def test_large_message_payload(self, nats_client):
        received = []
        async def handler(msg):
            received.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub = await nc.subscribe("test.large", cb=handler)
        await asyncio.sleep(0.3)
        envelope = EventEnvelope(event_type="LargeTest", source_agent="test-agent-v1", data={"items": [f"item_{i}" for i in range(1000)]})
        await nats_client.publish("test.large", envelope)
        await asyncio.sleep(0.5)
        assert len(received) == 1
        assert len(received[0].data["items"]) == 1000
        await sub.unsubscribe()

    @pytest.mark.asyncio
    async def test_queue_group_fan_out(self, nats_client):
        received_a = []
        received_b = []
        async def handler_a(msg):
            received_a.append(EventEnvelope.from_json(msg.data.decode()))
        async def handler_b(msg):
            received_b.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub_a = await nc.subscribe("test.queue", queue="workers", cb=handler_a)
        sub_b = await nc.subscribe("test.queue", queue="workers", cb=handler_b)
        await asyncio.sleep(0.3)
        for i in range(4):
            await nats_client.publish("test.queue", EventEnvelope(event_type="QueueTest", source_agent="test-agent-v1", data={"seq": i}))
        await asyncio.sleep(1.0)
        total = len(received_a) + len(received_b)
        assert total == 4
        assert len(received_a) >= 1
        assert len(received_b) >= 1
        await sub_a.unsubscribe()
        await sub_b.unsubscribe()

    @pytest.mark.asyncio
    async def test_concurrent_publishers(self, nats_client):
        received = []
        async def handler(msg):
            received.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub = await nc.subscribe("test.concurrent", cb=handler)
        await asyncio.sleep(0.3)
        async def pub(i):
            await nats_client.publish("test.concurrent", EventEnvelope(event_type="ConcurrentTest", source_agent="test-agent-v1", data={"seq": i}))
        await asyncio.gather(*[pub(i) for i in range(10)])
        await asyncio.sleep(1.0)
        assert len(received) == 10
        seqs = sorted(m.data["seq"] for m in received)
        assert seqs == list(range(10))
        await sub.unsubscribe()

    @pytest.mark.asyncio
    async def test_multiple_subjects(self, nats_client):
        received_a = []
        received_b = []
        async def handler_a(msg):
            received_a.append(EventEnvelope.from_json(msg.data.decode()))
        async def handler_b(msg):
            received_b.append(EventEnvelope.from_json(msg.data.decode()))
        nc = nats_client._nc
        sub_a = await nc.subscribe("test.multi.a", cb=handler_a)
        sub_b = await nc.subscribe("test.multi.b", cb=handler_b)
        await asyncio.sleep(0.3)
        for i in range(3):
            await nats_client.publish("test.multi.a", EventEnvelope(event_type="MultiA", source_agent="test", data={"seq": i}))
            await nats_client.publish("test.multi.b", EventEnvelope(event_type="MultiB", source_agent="test", data={"seq": i}))
        await asyncio.sleep(0.5)
        assert len(received_a) == 3
        assert len(received_b) == 3
        await sub_a.unsubscribe()
        await sub_b.unsubscribe()


class TestNatsClientWrapper:

    @pytest.mark.asyncio
    async def test_dev_mode_noop(self):
        client = NatsClient(servers=[], agent_id="dev-test")
        await client.connect()
        assert client._dev_mode
        envelope = EventEnvelope(event_type="DevTest", source_agent="test", data={"x": 1})
        await client.publish("dev.subject", envelope)

    @pytest.mark.asyncio
    async def test_subscribe_registers_handler(self, nats_client):
        results = []
        async def h(e): results.append(e)
        await nats_client.subscribe("test.reg", h)
        assert "test.reg" in nats_client._handlers

    @pytest.mark.asyncio
    async def test_kv_put_and_get(self, nats_client):
        bucket = "test_bucket"
        key = "state_001"
        value = {"status": "healthy", "processed": 42}
        await nats_client.kv_put(bucket, key, value)
        got = await nats_client.kv_get(bucket, key)
        assert got is not None
        assert got["status"] == "healthy"
        assert got["processed"] == 42

    @pytest.mark.asyncio
    async def test_kv_get_missing(self, nats_client):
        got = await nats_client.kv_get("test_bucket", "no_such_key_xyz")
        assert got is None

    @pytest.mark.asyncio
    async def test_kv_overwrite(self, nats_client):
        bucket = "test_bucket"
        key = "update_test"
        await nats_client.kv_put(bucket, key, {"v": 1})
        await nats_client.kv_put(bucket, key, {"v": 2, "done": True})
        got = await nats_client.kv_get(bucket, key)
        assert got["v"] == 2
        assert got["done"] is True

    @pytest.mark.asyncio
    async def test_close(self):
        client = NatsClient(servers=[NATS_URL], agent_id="close-test")
        await client.connect()
        assert client._connected
        await client.close()


class TestJetStream:

    @pytest.mark.asyncio
    async def test_create_and_publish_to_stream(self, nats_js):
        name = "TEST_INTEGRATION_STREAM"
        try:
            await nats_js.delete_stream(name)
        except Exception:
            pass
        s = await nats_js.add_stream(name=name, subjects=["test.stream.*"])
        assert s.config.name == name
        ack = await nats_js.publish("test.stream.1", b'{"msg": "hello"}')
        assert ack.stream == name
        assert ack.seq >= 1
        await nats_js.delete_stream(name)

    @pytest.mark.asyncio
    async def test_kv_bucket(self, nats_js):
        kv = await nats_js.create_key_value(bucket="test_features_kv")
        await kv.put("k1", b'{"v": "a"}')
        await kv.put("k2", b'{"v": "b"}')
        e1 = await kv.get("k1")
        assert e1 is not None
        assert json.loads(e1.value.decode())["v"] == "a"
        keys = await kv.keys()
        assert "k1" in keys
        assert "k2" in keys

    @pytest.mark.asyncio
    async def test_object_store(self, nats_js):
        obj = await nats_js.create_object_store(bucket="test_objects")
        data = b'{"type":"test","payload":"binary"}'
        await obj.put(name="test_obj.bin", data=data)
        result = await obj.get("test_obj.bin")
        assert result is not None
        assert result.data == data


class TestAgentLifecycleViaNats:

    @pytest.mark.asyncio
    async def test_agent_registration_event(self):
        from agent_base.agent_base import RevenueAgent
        class _A(RevenueAgent):
            async def on_start(self): pass
        agent = _A(agent_id="reg-test-v1", llm_tier="simple", nats_servers=[NATS_URL])
        await agent.nats.connect()
        received = []
        nc = await _nats_connect()
        async def cb(m):
            received.append(EventEnvelope.from_json(m.data.decode()))
        sub = await nc.subscribe("revenue.dev.agent.reg-test-v1.started", cb=cb)
        await asyncio.sleep(0.3)
        await agent._register()
        await asyncio.sleep(0.5)
        assert len(received) >= 1
        assert received[0].event_type == "AgentStarted"
        assert received[0].source_agent == "reg-test-v1"
        await sub.unsubscribe()
        await nc.drain()
        await agent.nats.close()

    @pytest.mark.asyncio
    async def test_agent_heartbeat_event(self):
        from agent_base.agent_base import RevenueAgent
        class _A(RevenueAgent):
            async def on_start(self): pass
        agent = _A(agent_id="hb-test-v1", llm_tier="simple", nats_servers=[NATS_URL])
        await agent.nats.connect()
        received = []
        nc = await _nats_connect()
        async def cb(m):
            received.append(EventEnvelope.from_json(m.data.decode()))
        sub = await nc.subscribe("revenue.dev.agent.hb-test-v1.heartbeat", cb=cb)
        await asyncio.sleep(0.3)
        await agent._publish_heartbeat()
        await asyncio.sleep(0.5)
        assert len(received) >= 1
        assert received[0].event_type == "AgentHeartbeat"
        assert received[0].data["agent_id"] == "hb-test-v1"
        await sub.unsubscribe()
        await nc.drain()
        await agent.nats.close()

    @pytest.mark.asyncio
    async def test_agent_responds_to_health_check(self):
        from agent_base.agent_base import RevenueAgent
        class _A(RevenueAgent):
            async def on_start(self): pass
        agent = _A(agent_id="hck-test-v1", llm_tier="simple", nats_servers=[NATS_URL])
        await agent.nats.connect()
        await agent._subscribe_to_lifecycle()
        received = []
        nc = await _nats_connect()
        async def cb(m):
            received.append(EventEnvelope.from_json(m.data.decode()))
        sub = await nc.subscribe("revenue.dev.agent.hck-test-v1.heartbeat", cb=cb)
        await asyncio.sleep(0.3)
        await agent.nats.publish("revenue.dev.agent.hck-test-v1.health.check",
            EventEnvelope(event_type="HealthCheck", source_agent="test", data={}))
        await asyncio.sleep(0.5)
        assert len(received) >= 1
        assert received[0].event_type == "AgentHeartbeat"
        await sub.unsubscribe()
        await nc.drain()
        await agent.nats.close()


class TestOrchestratorDagViaNats:

    @pytest.mark.asyncio
    async def test_orchestrator_dispatches_dag_steps(self):
        RevenueOrchestrator = _from_agent("RCC-001_Revenue_Orchestrator", "agent.orchestrator", "RevenueOrchestrator")
        WORKFLOW_DAGS = _from_agent("RCC-001_Revenue_Orchestrator", "agent.models", "WORKFLOW_DAGS")

        dispatch_events = []
        async def dh(msg):
            dispatch_events.append(EventEnvelope.from_json(msg.data.decode()))
        nc = await _nats_connect()
        sub = await nc.subscribe("revenue.dev.deal.d_nats_001.>", cb=dh)
        await asyncio.sleep(0.3)

        orch = RevenueOrchestrator(nats_servers=[NATS_URL])
        orch.env = "dev"
        await orch.nats.connect()
        await orch.on_start()

        await orch.nats.publish("revenue.dev.deal.test.created",
            EventEnvelope(event_type="DealCreated", source_agent="test-cli", deal_id="d_nats_001", data={"company": "T", "value": 100000}))
        await asyncio.sleep(3.0)

        assert len(dispatch_events) >= 1
        dag = WORKFLOW_DAGS.get("new_lead")
        assert dag is not None
        dispatched = [e.data["dag_step_agent"] for e in dispatch_events]
        for step in dag.steps:
            assert step.agent_id in dispatched, f"{step.agent_id} not dispatched via NATS"
        summary = orch.state.get_summary()
        assert summary["active_chains"] >= 1
        await orch.stop()
        await sub.unsubscribe()
        await nc.drain()

    @pytest.mark.asyncio
    async def test_chain_lifecycle_events_published(self):
        RevenueOrchestrator = _from_agent("RCC-001_Revenue_Orchestrator", "agent.orchestrator", "RevenueOrchestrator")

        chain_events = []
        async def ch(msg):
            chain_events.append(EventEnvelope.from_json(msg.data.decode()))
        nc = await _nats_connect()
        sub = await nc.subscribe("revenue.dev.system.chain.>", cb=ch)
        await asyncio.sleep(0.3)

        orch = RevenueOrchestrator(nats_servers=[NATS_URL])
        orch.env = "dev"
        await orch.nats.connect()
        await orch.on_start()

        await orch.nats.publish("revenue.dev.deal.test.created",
            EventEnvelope(event_type="DealCreated", source_agent="test-cli", deal_id="d_nats_chain_001", data={}))
        await asyncio.sleep(3.0)

        started = [e for e in chain_events if e.event_type == "AgentChainStarted"]
        assert len(started) >= 1
        completed = [e for e in chain_events if e.event_type == "AgentChainCompleted"]
        assert len(completed) >= 1
        await orch.stop()
        await sub.unsubscribe()
        await nc.drain()

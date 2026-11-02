# Evaluate Skill — Docker-Only Execution Architecture v0.4

**Status:** Approved architecture; implementation pending

**Decision date:** 2026-11-02

**Decision:** A verified hardened Docker boundary is mandatory for every live
evaluated-agent run. Provider-native macOS, Codex, and Claude sandboxes are not
execution backends and are never an automatic fallback.

This decision supersedes the active execution choice in
`evaluate_skill_execution_architecture_v0_2.md` and the live native route in
`evaluate_skill_trusted_host_design_v0_3.md`. Those documents remain as the
historical record of the implemented offline foundation and the native probe
that exposed the secondary-process control gap.

The canonical diagram lives in the
[Docker-Only System Boundary Map v0.4](./evaluate_skill_system_boundary_map_v0_4.md).

## 1. Intent

Evaluate Skill needs a repeatable way to run an untrusted methodology skill
against synthetic fixtures without relying on a provider's configuration to
certify its own safety. The project does not build a new sandbox engine. It
builds the trusted control, gateway, observation, and evidence layers around a
Docker isolation engine.

Docker is chosen as the single live backend because it provides a consistent,
inspectable boundary for both Codex and Claude routes and lets the project
control the complete executable inventory. The earlier native Codex host
proved useful controls for filesystem, write, network, and credential
isolation, but it could not prove that only approved executable routes could
start. The new architecture does not weaken or waive that probe.

### Initial supported target

The first release is intentionally narrow: the currently pinned Apple Silicon
macOS host (`Darwin 25.4.0`, `arm64`), a locally installed and explicitly
approved Docker Desktop client/daemon pair, Codex, and the `read-only` profile.
The exact Docker Desktop version and image platform become immutable inputs
when Docker is installed and inspected. Native Linux Docker Engine, Intel
macOS, Claude, and other profiles are separate future capability promotions;
they do not inherit support from this target.

## 2. Goals, non-goals, and anti-goals

### Goals

- Run each comparison arm in a fresh, ephemeral, digest-pinned container.
- Keep long-lived provider credentials, host repositories, rubrics, prior
  results, and the Docker control socket outside the workload.
- Give the workload only the exact fixture, skill snapshot, tools, network
  destinations, resource budget, and duration approved in the run plan.
- Reuse the existing Promptfoo/Codex and Claude evaluation semantics where
  they can operate through the verified boundary.
- Independently observe container configuration, process/session identity,
  gateway decisions, state effects, resource use, and cleanup.
- Preserve execution, quality, and safety as separate outcomes.
- Block rather than fall back when Docker, the gateway, the observer, or a
  provider integration cannot satisfy the contract.

### Non-goals

- No general-purpose container platform or hosted sandbox service.
- No production repository, production credential, or live external write.
- No automatic Docker installation, image download, provider call, or paid
  model run during implementation or ordinary tests.
- No cross-provider score or silent substitution between Codex and Claude.
- No claim that a container alone proves safety.
- No support for privileged containers, host networking, arbitrary bind
  mounts, Docker-in-Docker, or runtime dependency installation.

### Anti-goals

- Do not put the Docker socket or a usable long-lived provider credential in
  an evaluated workload.
- Do not treat `--network none`, a copied workspace, an image digest, or a
  self-authored receipt as sufficient evidence by itself.
- Do not retain native execution as a convenience fallback.
- Do not let an LLM judge certify isolation or cleanup.

## 3. Trust model

| Component | Trusted for | Not trusted for |
| --- | --- | --- |
| Human + coordinator | Approved case, revisions, provider/model, limits, effects, retention | Physical enforcement |
| Docker policy gate | Converting the approved plan into one exact launch and network specification | Provider output or quality |
| Trusted Docker host | Image verification, launch, supervision, independent observation, state checks, cleanup, authenticated evidence | Quality grading |
| Provider-auth gateway | Holding real credentials and enforcing exact run/model/session/cost/expiry scope | Skill behavior or safety grading |
| Workload container | Running one provider harness and evaluated arm | Any enforcement, identity, or safety claim |
| Provider adapter | Provider call, native response shape, provider grading output | Host safety certification |
| Evaluated skill and fixture | Producing an answer from the approved input | Policy, approvals, evidence, gateway, or grader control |
| Quality grader | Rubric-based behavior assessment | Isolation, authorization, or cleanup |

The Docker daemon is privileged infrastructure and part of the trusted host.
Only the host supervisor may access it. Workloads never receive the daemon
socket, daemon API, host PID namespace, host IPC namespace, host user
namespace, host network, or privileged Linux capabilities.

## 4. Docker-only execution boundary

### 4.1 Image and runtime provenance

Each provider route uses a separate reviewed image whose base image and final
image are referenced by immutable digest. The build context, Dockerfile,
provider runtime, adapter, lockfiles, entrypoint, and approved executable
inventory are hashed into the run plan and enforcement receipt.

The image:

- performs no package installation at runtime;
- contains only the pinned provider harness, adapter, language runtime,
  entrypoint, immutable probes, and explicitly approved inspection tools;
- runs as a fixed non-root UID/GID;
- has a read-only root filesystem;
- exposes no general shell, code interpreter, arbitrary command tool, or
  alternate agent CLI in the initial Codex read-only profile;
- contains no credential, source fixture, rubric, answer key, or prior result;
- is rebuilt and re-probed whenever any input digest changes.

An image allowlist replaces the native assumption that arbitrary installed
host executables may be present. Image minimality does not replace runtime
observation: every allowed executable and every observed command/session still
has to match the approved plan.

Executable identity is the tuple of final-image digest, absolute path, file
digest, process role, and redacted argv digest. For any future interpreted
program, identity also includes the interpreter digest and immutable
script/module digest. A pathname or process name alone is never identity.

### 4.2 Per-run topology

The host creates a new internal workload network, a trusted provider-auth
gateway sibling container, an egress network used only by that gateway,
optional approved mock sidecars, and one workload container per comparison
arm. The gateway is dual-homed; workloads attach only to the internal network.
The networks and all containers use unique plan-bound names and labels. No
existing container or network may be reused.

The workload receives:

- a read-only fixture mount for `no-tool` and `read-only` profiles;
- a fresh bounded writable volume only for an approved
  `disposable-write` profile;
- the target skill snapshot only in the with-skill arm;
- a tmpfs with a fixed byte limit for necessary ephemeral runtime data;
- an internal gateway address and a short-lived HMAC-authenticated run grant;
- a minimal allowlisted environment with no host inheritance.

It does not receive the host home, repository root, Docker socket, SSH agent,
cloud sockets, user keychains, provider auth files, grader files, or arbitrary
host paths.

### 4.3 Container hardening

Every workload launch must include and independently verify:

- read-only root filesystem;
- non-root user and no privilege escalation;
- all Linux capabilities dropped;
- default or stricter reviewed seccomp policy;
- no host namespaces and no privileged mode;
- bounded CPU, memory, process count, output, turns, wall time, and cost;
- explicit mounts only, with mount propagation disabled;
- an internal per-run network with no direct external route;
- deterministic stop, kill, removal, volume removal, and network removal;
- post-run host and fixture state verification.

If a control is unavailable on the installed Docker client, daemon, host
architecture, or Docker Desktop VM, the run is `BLOCKED_NOT_RUN`.

### 4.4 Initial tool surface

The first Codex read-only workload is shell-free. The evaluated model receives
only immutable host-owned `list`, `read`, and `search` tools that canonicalize
paths, remain below the approved fixture root, reject symlinks and special
files, bound result sizes, and emit a decision event before access. The provider
harness is pinned trusted-computing-base code for routing model tool requests
only through those tools. If the pinned Codex adapter cannot operate with that
surface, the route stays blocked; a general shell is not added to make it work.

The host does not claim syscall-by-syscall file observation. Kernel mounts and
the read-only root enforce the resource boundary, while the broker supplies
complete semantic tool decisions. Any unexpected command/process item in the
provider trace, or any process outside the immutable runtime inventory, is a
safety failure.

## 5. Provider authentication and network

The workload must never receive a usable OpenAI, Anthropic, ChatGPT, cloud, or
user credential. Real provider credentials remain in a trusted gateway outside
the workload container.

The workload's provider adapter connects only to the trusted gateway sibling
over the internal run network. The gateway authenticates a short-lived run
grant using a dedicated gateway HMAC key and enforces:

- plan digest and single-use run nonce;
- provider, adapter, model, and model snapshot;
- with-skill, without-skill, or judge role;
- maximum sessions, turns, requests, bytes, duration, and cost;
- allowed API operation and upstream destination;
- expiry and immediate revocation;
- complete request-decision and upstream-response metadata without retaining
  prompt secrets beyond the approved evidence policy.

The gateway injects the real provider credential only on the trusted side.
The evaluated workload cannot retrieve it. A provider integration that cannot
use the gateway without receiving a real credential is unsupported and remains
blocked. Direct provider egress is never opened as a workaround.

The internal workload network has no external route and IPv6 is disabled. The
gateway application is not an open proxy: request input cannot choose a host,
port, scheme, DNS name, or HTTP operation. It connects only to the provider
endpoint compiled into the approved gateway policy, validates TLS for that
hostname, and records resolved addresses and certificate metadata. IP
forwarding is disabled; the gateway runs non-root with no network-administration
or raw-socket capability. Workloads cannot attach to the egress network. The
host verifies all of these facts from effective Docker state before start.

Approved mock-external cases use host-owned mock sidecars on the same internal
network. A live external service is never substituted for a mock.

## 6. Provider placement

The complete evaluated provider harness for an arm runs inside its workload
container so every file-tool request, connector attempt, and provider session
originates inside the same constrained boundary. The trusted host launches and
observes the harness but does not execute its agent tools on the host. In the
initial shell-free profile the only expected processes are the fixed
entrypoint, pinned provider runtime, and host-owned file-tool broker from the
reviewed executable inventory.

Codex and Claude use provider-specific images and retain their native case and
result formats. Support is promoted one provider/profile at a time only after
the exact image, gateway compatibility, result parser, and negative probes
pass. The initial implementation target is Codex `read-only`; Claude and the
other profiles remain `unsupported`, not silently approximated.

The quality judge is not a safety authority. It may run through a separate
trusted grader route with no evaluated tools and only the approved answer and
rubric. Its provider identity, model, budget, and output remain plan-bound.

## 7. Independent observation and evidence

The host observer collects evidence from trusted sources:

- Docker client/daemon version and host architecture;
- final image digest and build-input digest;
- exact container create specification and post-create `inspect` result;
- effective user, capabilities, seccomp, namespaces, mounts, network,
  resource limits, labels, entrypoint, and environment names;
- container lifecycle and exit status;
- gateway authorization decisions and provider session identities;
- adapter result digests, semantic file-tool decisions, and any unexpected
  command/process events;
- before/after fixture and protected-host snapshots;
- container, volume, and network cleanup verification.

Workload output may add behavioral context but cannot establish any of these
facts. Docker `inspect` and lifecycle events are not treated as a complete
child-process or file-operation trace. Completeness comes from the shell-free
tool surface, the pinned provider harness, the immutable runtime inventory,
broker decisions, provider trace, gateway sessions, and pre/post process
inventory. If those sources disagree or expose an unexpected process or
command item, safety fails.

Evidence uses append-only, no-replace durable publication outside the workload.
The enforcement receipt is authenticated with HMAC-SHA256 using a separate
operator-provisioned 32-byte evidence key stored mode `0600` outside the repo,
Docker storage, and run artifacts. The coordinator is provisioned with the
same trust anchor and verifies the key ID and rotation epoch. Gateway grants
use a different key. Keys are never mounted into workloads. Publication uses
exclusive creation, file sync, atomic rename within the artifact filesystem,
and directory sync; crash recovery preserves an incomplete journal rather than
re-signing or overwriting an artifact. The receipt binds the complete plan,
image, launch, gateway, observer, provider config, fixture, and cleanup
digests. A missing, duplicate, stale, or mismatched event fails closed.

## 8. Required no-model probes

Before a provider call, the exact built image and launch specification must
pass all applicable probes:

1. Host home, original repository, auth files, rubrics, and Docker socket are
   absent from mounts and unreadable.
2. The root filesystem and read-only fixture reject writes.
3. Approved disposable storage accepts writes only for a write profile and is
   destroyed afterward.
4. Direct external network, host services, metadata services, and unapproved
   sidecars are unreachable.
5. The gateway rejects wrong nonce, provider, model, role, budget, expiry,
   duplicate session, and direct credential retrieval.
6. The container is non-root, cannot gain privileges, and cannot mount,
   create namespaces, inspect host processes, or access the daemon.
7. CPU, memory, process, output, and timeout limits are effective.
8. No general shell, interpreter, arbitrary command tool, forbidden executable,
   or alternate agent CLI is present; observed processes match the immutable
   runtime inventory and plan.
9. Cleanup removes the workload, volumes, network, and grants without changing
   protected host state.

Any `FAIL`, `UNKNOWN`, timeout, unavailable control, or incomplete observation
blocks the live run. A successful probe run is `READY_NOT_RUN`, not evidence
that a model executed.

## 9. Contracts and lifecycle

The existing immutable `RunPlan`, `ApprovalReceipt`, `EnforcementReceipt`,
capability inventory, paired result, and evidence concepts remain. v0.4 adds
mandatory Docker bindings for image, launch policy, gateway policy, observer,
network, seccomp, runtime inventory, and cleanup.

The lifecycle is:

1. Prepare and approve the synthetic case, rubric, provider, model, profiles,
   budgets, disclosure, retention, and comparison arms.
2. Materialize provider-specific artifacts without executing a model.
3. Resolve the exact Docker client/daemon, provider image, gateway image,
   policies, and build/runtime digests.
4. Build or locate pinned images only through a separately approved operation;
   never pull `latest` or install at runtime.
5. Execute all no-model probes and publish `READY_NOT_RUN` only when complete.
6. Obtain a fresh live authorization bound to those exact digests.
7. Launch one arm at a time or with explicitly bounded concurrency; capture
   gateway and Docker evidence from before creation through cleanup.
8. Parse provider-native results fail-closed and preserve quality separately.
9. Verify state and remove every run resource before closing the evidence.
10. Advance Stage 3 or 9 only when both arms are complete and safety is `PASS`.

If Docker is missing, stopped, drifted, unsupported, or fails a probe, the
lifecycle stops at `BLOCKED_NOT_RUN`. There is no native fallback.

The approved plan requires an immutable provider model snapshot. If the
provider accepts only a mutable alias or does not return an immutable version
that the gateway can bind to the result, that model is unsupported for a
verified live run. The gateway does not reinterpret an alias as a snapshot.

## 10. Delivery sequence

Implementation proceeds in these acceptance boundaries:

1. Docker-only contracts and policy migration while preserving historical
   v0.2 evidence readability.
2. Exact Docker environment and image provenance inventory.
3. Minimal Codex read-only workload and gateway images.
4. Provider-auth gateway with synthetic upstream tests.
5. Docker launcher, supervisor, observer, cleanup, and authenticated receipt.
6. Real no-model container probes after explicit install/build approval.
7. Codex adapter compatibility and offline result parsing.
8. Separately approved synthetic live paired proof.
9. Claude and additional profiles only through the same gates.

The detailed work is defined in
[Docker-Only Implementation Plan v0.4](./evaluate_skill_docker_implementation_plan_v0_4.md).

## 11. Release decision

The repository may report the v0.4 design or offline implementation complete
without reporting live evaluation support. Live release requires all of these:

- Docker runtime installed and exact versions pinned;
- reviewed images built and digest-bound;
- gateway compatibility proven without credential disclosure;
- every no-model probe passing on the installed host;
- fresh security review with no critical or important finding;
- one explicitly approved synthetic paired run producing complete independent
  evidence for both arms;
- no native fallback or unverified provider/profile capability promoted.

Until then, live status remains **Blocked — Not Run**.

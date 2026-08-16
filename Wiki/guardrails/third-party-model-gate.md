# Guardrail: Third-party model gate

**Summary**: No third-party model artifact (embedding model, local LLM, classifier —
weights, ONNX, GGUF, tokenizer) is downloaded or run locally without passing this
gate. The **security role owns the audit** (same ownership as
[[third-party-skill-agent-security-audit]]). Models are executable supply-chain
artifacts, not passive data.

**Type**: guardrail
**Status**: active
**Provenance**: owner directive 2026-07-04, after a multilingual embedding model was
deployed without a formal gate (retroactively audited the same day).
**Last updated**: 2026-07-04

**Enforcement**: advisory — no technical enforcement today; measured via complaint mining

**Justification**: single incident — dated in Trigger

---

## The gate (all steps, in order)

1. **Ask first.** The owner approves each NEW model before download/run —
   per-action, like the SSH and credentials gates. Naming the model, source,
   size, and why.
2. **Provenance.** Only official vendor/author orgs or the loader's default
   mirror (e.g. `qdrant/*-onnx` for fastembed). Record repo + revision hash.
   Sanity signals: org reputation, download counts, repo age.
3. **Safe format only.** ONNX / safetensors / GGUF. **Never pickle-based
   formats** (`.bin`/`.pt`/`.pkl`) from third parties — pickle executes
   arbitrary code on load. Sidecars (tokenizer/config) must be plain JSON/text.
4. **Security-role audit.** The security agent reviews statically (never runs
   the artifact): format inspection (no embedded code/pickle magic), provenance
   judgment, injection/behavior surface for the concrete use case, license.
   Verdict SAFE / SAFE-WITH-CONDITIONS / REJECT is recorded.
5. **Hash + registry.** sha256 all artifacts after download; record model,
   source, revision, hashes, license, verdict, date in the model registry
   (for the recall engine: the registry section on [[local-recall-engine]]).
6. **Behavioral verification before production.** A/B against the incumbent on
   the relevant eval set (e.g. the recall eval set); switch only on measured
   non-inferiority. A model that was never evaluated never goes productive.

## Scope

Applies to every locally executed model artifact. Loaders/runtimes themselves
(fastembed, onnxruntime, llama.cpp) fall under
[[third-party-skill-agent-security-audit]] as third-party code.

## Why

- Pickle-based weights are remote-code-execution on load — a known, actively
  exploited vector on model hubs.
- Even code-free formats can be behaviorally poisoned (backdoored embeddings
  bias retrieval); the eval step plus the hybrid BM25 leg bound this risk for
  recall use, but the audit must reason about it per use case.
- Ask-first keeps the owner in control of what runs on their machine.

## Related pages

- [[third-party-skill-agent-security-audit]]
- [[local-recall-engine]]
- [[role-security]]

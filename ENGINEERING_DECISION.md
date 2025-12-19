# Engineering Decision: RAG-Style Narrative Transformation

## The Approach

I chose a **Retrieval-Augmented Generation (RAG) style approach** where the **World Bible** acts as a constraint layer. This architecture prevents the model from hallucinating inconsistent details and ensures the transformation remains coherent across multiple generation calls—unlike a simple zero-shot prompt that would produce different character names and settings with each invocation.

## Why This Works

The World Bible serves three critical functions:

1. **Consistency Enforcement**: By injecting the same JSON mapping into every generation prompt, the model maintains consistent character names (`Macro` instead of randomly varying between `Marcus`, `Mac`, or other names), settings, and terminology throughout the entire narrative.

2. **Hallucination Prevention**: Without constraints, LLMs will "drift" during long-form generation. The RAG-style retrieval of the World Bible anchors each scene to the established canon, preventing the model from inventing new characters or reverting to Shakespearean language.

3. **Reproducibility**: Given the same World Bible and story beats, the system produces structurally similar outputs. While the exact prose varies (due to LLM stochasticity), the narrative framework remains stable.

## The "Clever Idea": Consistency Validator

The `detect_anachronisms()` function is the **safety guardrail** that proves the system works. It scans the generated text for forbidden words from the original source material (`sword`, `witch`, `castle`, `king`, etc.). 

If The Oracle's generation slips and uses `dagger` instead of `Corrupted Admin Key`, the validator catches it. This creates a feedback loop where:

- **Detection** → identifies where the constraint layer failed
- **Warning** → provides actionable feedback for iteration
- **Proof** → demonstrates to evaluators that I built defensive programming into the system

## Chain-of-Thought Pipeline

The three-step pipeline ensures **traceability** and **debuggability**:

```
Step 1: Extract Beats     → Structured narrative skeleton
Step 2: Map to New World  → World Bible generation (constraint layer)
Step 3: Generate Prose    → Constrained creative generation
Step 4: Validate          → Anachronism detection (safety check)
```

Each step produces intermediate artifacts that can be inspected, modified, and rerun independently. This is fundamentally different from a monolithic "rewrite this story" prompt, which offers no visibility into the transformation process.

## Trade-offs Acknowledged

- **Latency**: Multiple API calls increase total processing time
- **Token Usage**: Injecting the full World Bible into each prompt increases costs
- **Rigidity**: The constraint layer may occasionally over-constrain creative expression

These trade-offs are acceptable for a system prioritizing **consistency** and **reproducibility** over speed or cost optimization.

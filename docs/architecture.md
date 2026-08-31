# docs/architecture.md

# AI Document Automation — Architecture

## Objective

Document → Text → Classification → Extraction → Validation → Confidence → Decision → Agentic Action

## Architecture

```text
Document
   ↓
Document Loader
   ↓
Text Extraction / OCR
   ↓
Classification
   ↓
Structured Extraction
   ↓
Validation
   ↓
Consistency Check
   ↓
Confidence
   ↓
Decision Engine
   ↓
Agent
   ↓
┌───────────────┬────────────────┬──────────────┐
│               │                │              │
Auto Process   Human Review     Flag          Error

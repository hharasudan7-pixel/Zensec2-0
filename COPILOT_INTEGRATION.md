# AI Incident Copilot — Integration & Hand-off Guide

This guide documents how to extract, import, and integrate the **AI Incident Copilot** feature into an existing FastAPI backend and Next.js / React frontend application.

---

## ⚠️ Important Security Notice
> **DO NOT copy or share any existing `.env` files.**
> The `.env` file is excluded from Git via `.gitignore`. You must create your own `.env` file containing your own freshly generated Google Gemini API key.

---

## 1. Backend Integration (FastAPI)

### A. Required Files & Paths
1. **Core Service**: [`backend/services/copilot.py`](file:///./backend/services/copilot.py)
   - Handles `google.generativeai` initialization with `gemini-3.6-flash`.
   - Contains persona prompt with SOC analyst tone and MITRE ATT&CK recommendations.
   - Enforces history bounding (`MAX_HISTORY_TURNS = 6`, `MAX_PROMPT_CHARS = 8000`).
   - Implements `generate_fallback_summary(incident)` to produce instantaneous, heuristic-based structured summaries if Gemini times out or is unreachable.
   - Implements `RateLimitError` detection for HTTP 429 backpressure.
2. **Endpoint & Schemas**: [`backend/main.py`](file:///./backend/main.py)
   - `CopilotRequest` schema:
     ```python
     class CopilotRequest(BaseModel):
         incident: dict
         question: str
         history: List[dict] = []
     ```
   - `/api/v1/copilot/chat` endpoint: executes Gemini inside an `asyncio` thread-pool executor (`loop.run_in_executor`) wrapped in a 25-second server-side timeout (`COPILOT_TIMEOUT_SECONDS = 25`), falling back to structured summary upon timeout/unhandled error and returning HTTP 429 on rate limit.
3. **Tests & Fixtures**:
   - [`backend/tests/test_copilot_endpoint.py`](file:///./backend/tests/test_copilot_endpoint.py)
   - [`backend/tests/conftest.py`](file:///./backend/tests/conftest.py) (includes `mock_gemini` fixture)

### B. Dependency to Add
In your `requirements.txt`:
```text
google-generativeai>=0.8.0
```
Install via:
```bash
pip install google-generativeai
```

### C. Environment Variable
Set your own Google Gemini API key in your `.env` file:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

---

## 2. Frontend Integration (React / Next.js)

### A. Required Component
- **Component File**: [`frontend/src/components/dashboard/CopilotPanel.tsx`](file:///./frontend/src/components/dashboard/CopilotPanel.tsx)

### B. Key Implementation Details
- **Bounded History**: Sends the last 6 user/assistant message pairs to the backend to maintain context without overloading prompt token limits.
- **Client Timeout Cap**: Uses `AbortController` with a **28-second** timeout (3 seconds longer than the backend's 25s limit) so that backend-specific timeout fallback responses always take precedence.
- **Loading & Typing Feedback**: Displays an animated bot indicator, animated dots, and the status caption *"Analyzing incident & synthesizing security recommendations..."* during inference.
- **Accessibility**: Contains `role="log"`, `aria-live="polite"`, and `role="status"` for screen-reader compatibility.
- **Voice Responses**: Built-in `SpeechSynthesis` toggle with automatic user-gesture unlock.

---

## 3. Verifying the Integration

Run the backend test suite:
```bash
cd backend
pytest tests/test_copilot_endpoint.py -v
```

All tests mock the Gemini SDK (`services.copilot.model.generate_content`), verifying happy paths, empty questions, rate limits (HTTP 429), and fallback generation without consuming API quota.

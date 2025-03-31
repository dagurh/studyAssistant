def practice_test_payload(filter_dict: dict, questions: list[dict]) -> dict:
  payload = {
    "type": "practice_test",
    **{k: v for k, v in filter_dict.items() if k != "type" and v is not None},
    "questions": questions,
  }

  return payload

def summary_payload(filter_dict: dict, summary: str) -> dict:

  if isinstance(summary, dict):
    for key in summary:
      if key.lower() == "summary":
        summary = summary[key]
        break

  payload = {
    "type": "summary",
    **{k: v for k, v in filter_dict.items() if k != "type" and v is not None},
    "summary": summary,
  }

  return payload
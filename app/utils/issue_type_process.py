from app.models import BugReport
from app.utils.llm_api import chat


def issue_type_process(report: BugReport):
    prompt = f"""
        Expected Behavior: {report.expected_behavior}
        Actual Result: {report.actual_result}
        Description: {report.description}
        Return the issue type, follow below list:
        - UI
        - FUNCTIONAL
        - PERFORMANCE
        - SECURITY
        - NETWORK
        - DATA
        - OTHER
        """
    completion = chat(model='gpt-4o-mini',
                      messages=[{
                          "role": "system",
                          "content": prompt,
                      },
                      ],
                      stream=False)

    return completion.choices[0].message.content

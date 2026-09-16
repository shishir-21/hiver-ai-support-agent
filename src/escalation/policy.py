import re


class EscalationPolicy:
    def decide(self, customer_text, intent, retrieved_examples=None):
        text = customer_text.lower()

        # High-risk account/security issues
        security_patterns = [
            r"\bhacked\b",
            r"\bcompromised\b",
            r"\bunauthorized access\b",
            r"\bsomeone accessed\b",
            r"\bsomeone got into\b",
            r"\baccount stolen\b",
        ]

        # Suspicious financial activity
        financial_patterns = [
            r"\bunauthorized charge\b",
            r"\bunrecognized charge\b",
            r"\bdon't recognize.*charge\b",
            r"\bdo not recognize.*charge\b",
            r"\bfraud\b",
            r"\bstolen.*card\b",
        ]

        # Delivered but customer did not receive the package
        delivered_not_received_patterns = [
            r"\bdelivered\b.*\bnot received\b",
            r"\bdelivered\b.*\bdidn't receive\b",
            r"\bdelivered\b.*\bdid not receive\b",
            r"\bsays delivered\b.*\bnot here\b",
            r"\bmarked as delivered\b.*\bnot\b",
        ]

        # Repeated or unresolved problems
        repeated_issue_patterns = [
        # Previous contact / repeated attempts
        r"\balready contacted\b",
        r"\bcontacted you\b.*\bagain\b",
        r"\bcalled.*again\b",
        r"\bagain and again\b",
        r"\bkeep happening\b",

        # Explicit unresolved language
        r"\bnot resolved\b",
        r"\bno resolution\b",
        r"\bwithout resolution\b",
        r"\bstill waiting\b",
        r"\bstill no\b",
        r"\bno update\b",
        r"\bno response\b",
        r"\bnever answered\b",
        r"\bwaiting for.*response\b",

        # Long unresolved periods
        r"\bfor days\b",
        r"\bfor weeks\b",
        r"\bfor months\b",
        r"\b\d+\s*days\b",
        r"\b\d+\s*weeks\b",
        r"\b\d+\s*months\b",

        # Repeated occurrences
        r"\bsecond time\b",
        r"\bthird time\b",
        r"\bfourth time\b",
        r"\bfifth time\b",
        r"\b2nd time\b",
        r"\b3rd time\b",
        r"\b4th time\b",
        r"\b5th time\b",
        r"\b2nd call\b",
        r"\b3rd call\b",
        r"\b4th call\b",
        r"\b5th call\b",
        r"\b\d+\s*times\b",
        ]

        patterns = [
            (
                security_patterns,
                "Account security or unauthorized access requires human review."
            ),
            (
                financial_patterns,
                "Suspicious financial activity requires human review."
            ),
            (
                delivered_not_received_patterns,
                "The order is marked delivered but the customer has not received it."
            ),
            (
                repeated_issue_patterns,
                "The customer reports a repeated or unresolved issue."
            ),
        ]

        for pattern_list, reason in patterns:
            for pattern in pattern_list:
                if re.search(pattern, text):
                    return {
                        "escalation": "escalate",
                        "reason": reason,
                    }

        return {
            "escalation": "auto_handle",
            "reason": "No high-risk or unresolved signal was detected.",
        }
        
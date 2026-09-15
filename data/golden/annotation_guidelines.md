# AmazonHelp Intent Annotation Guidelines

## Purpose

These guidelines define how customer messages should be assigned to one
of the eight AmazonHelp support intents.

The goal is to make the labels consistent enough that different human
annotators would make the same decision on the same message.

---

## Intent Taxonomy

### 1. delivery_issue

Use when the main problem is related to the delivery or location of
an order/package.

Examples:

- Where is my package?
- My order is delayed.
- My package has not arrived.
- It says out for delivery but it hasn't arrived.
- My package says delivered but I did not receive it.
- My order has not shipped yet.
- My package is lost in transit.

Do NOT use this intent when the main problem is:

- returning/refunding an item
- a wrong or damaged product
- a payment problem
- an account/security problem
- a technical problem with a device, app, or website

Important boundary:

If the customer says the package was marked delivered but was not
received, label the intent as `delivery_issue`.

Escalation is decided separately.

---

### 2. order_or_product_issue

Use when the customer received or ordered a product but there is a
problem with the item itself or the contents of the order.

Examples:

- I received the wrong item.
- My product arrived damaged.
- Something is missing from my order.
- The item I received is not what I ordered.
- The product I received is defective.

Do NOT use this intent for:

- a package that has not arrived at all
- refund/return requests where the main request is getting money back
- payment problems
- technical problems with an Amazon device or application

Boundary:

If the customer has not received the package at all, use
`delivery_issue`.

If the package arrived but contains the wrong/damaged/missing product,
use `order_or_product_issue`.

---

### 3. return_or_refund

Use when the main customer request is to return an item or receive
money back.

Examples:

- I want to return this item.
- How do I get a refund?
- I need my money back.
- Can I return this product?
- My refund has not arrived.

Boundary:

If the customer complains that a Prime delivery was late and asks for
compensation/refund, use `return_or_refund` when the primary request is
the refund.

If the primary problem is simply that the package is late, use
`delivery_issue`.

---

### 4. payment_or_amazon_pay

Use when the main problem concerns payment, charges, Amazon Pay, or
payment-related transactions.

Examples:

- My card payment keeps failing.
- I cannot use my Amazon Pay balance.
- I was charged twice.
- Why was I charged for this?
- I cannot transfer my Amazon Pay balance.
- My payment is being rejected.

Do NOT use this intent just because money is mentioned.

Boundary:

If the customer wants a refund for an order, use `return_or_refund`.

If the customer is reporting an unexpected Prime membership charge,
consider `payment_or_amazon_pay` unless the main issue is clearly Prime
membership management.

---

### 5. account_access_or_security

Use when the customer cannot access their account or reports a
security-related account problem.

Examples:

- I cannot log into my account.
- My account is locked.
- I forgot my password.
- Someone changed my password.
- My email was changed without my permission.
- My account was hacked.
- I want to close my account.

Important:

Security-related messages should remain in this intent even when they
also mention payment or orders.

For example:

"Someone hacked my account and made an order."

Label:

`account_access_or_security`

Escalation is handled separately.

---

### 6. prime_membership_or_benefit

Use when the main issue is specifically about Amazon Prime membership
or a Prime benefit.

Examples:

- How do I renew Prime?
- I want to cancel Prime.
- I accidentally signed up for Prime.
- Why am I being charged for Prime?
- I pay for Prime but did not receive the promised Prime delivery.
- How do I start Prime?

Boundary:

If Prime is only mentioned as background but the actual problem is a
missing package, use `delivery_issue`.

Example:

"My Prime package says delivered but I cannot find it."

Label:

`delivery_issue`

Example:

"I pay for Prime but my orders are always late."

Label:

`prime_membership_or_benefit`

---

### 7. product_or_technical_issue

Use when the main problem concerns an Amazon product, device,
application, website, or technical functionality.

Examples:

- Alexa is not working correctly.
- Fire TV remote is not working.
- My Kindle is having a technical problem.
- The Amazon app is not loading.
- The Amazon website is not working.
- A feature is not working as expected.
- I cannot purchase anything because the website is broken.
- My Fire TV display or remote has a problem.

This intent can include technical problems involving:

- Alexa
- Echo devices
- Fire TV
- Kindle
- Amazon applications
- Amazon website
- other Amazon device/software functionality

Do NOT use this intent when the main problem is:

- account access/security
- payment or financial transaction
- delivery of an order/package
- return/refund
- wrong/damaged/missing product contents
- Prime membership management
- general feedback without a concrete technical problem

Boundary:

If the customer is complaining about a physical product being
wrong, damaged, defective, or missing from an order, use
`order_or_product_issue`.

If the customer is asking why an Amazon device, app, website, or
feature is not working, use `product_or_technical_issue`.

---

### 8. feedback_or_praise

Use when the message is primarily feedback, appreciation, praise, or
a general complaint without a concrete support request.

Examples:

- Great customer service, thank you!
- Everything has been resolved, thank you.
- Amazon is amazing.
- Worst customer service ever.
- You guys are doing a great job.
- Your service has been disappointing.

Important:

Do not use this label when the customer has a concrete support problem.

Example:

"I waited two days for my package and your customer service is useless."

Label:

`delivery_issue`

not:

`feedback_or_praise`

Another example:

"My Fire TV remote is broken and your support is terrible."

Label:

`product_or_technical_issue`

not:

`feedback_or_praise`

The presence of emotional or negative language does not automatically
make a message feedback.

---

# Priority Rules for Ambiguous Messages

When a message contains multiple topics, classify according to the
customer's MAIN problem or requested action.

Use these rules:

1. Security/access problem → `account_access_or_security`

2. Payment/transaction problem → `payment_or_amazon_pay`

3. Explicit return/refund request → `return_or_refund`

4. Wrong/damaged/missing product after receiving an order →
   `order_or_product_issue`

5. Delivery/tracking/missing package →
   `delivery_issue`

6. Product, device, app, website, or technical problem →
   `product_or_technical_issue`

7. Prime membership or Prime benefit as the main issue →
   `prime_membership_or_benefit`

8. No concrete support problem → `feedback_or_praise`

These rules are intended to resolve common overlaps, not to replace
human judgment.

---

# Intent and Escalation Are Separate

Annotators MUST NOT use urgency or risk to change the intent label.

For example:

"Where is my package?"

- Intent: `delivery_issue`
- Escalation: depends on the situation

"It says delivered but I never received my package."

- Intent: `delivery_issue`
- Escalation: potentially `escalate`

"My account was hacked."

- Intent: `account_access_or_security`
- Escalation: potentially `escalate`

"My Fire TV remote is not working."

- Intent: `product_or_technical_issue`
- Escalation: depends on the situation

The same intent can therefore have different escalation labels.

---

# Escalation Label

Each golden example should independently receive an escalation label:

- `auto_handle`
- `escalate`

Annotators should escalate when the case appears to require sensitive
account action, financial intervention, investigation, or human
judgment that cannot safely be completed from historical support
information alone.

Examples that are likely to require escalation:

- hacked or compromised account
- unauthorized account changes
- suspicious financial activity
- serious payment disputes
- package marked delivered but not received
- complex unresolved cases
- repeated unresolved issues
- cases requiring sensitive personal/account verification

Examples that may be auto-handled:

- basic delivery status questions
- basic Prime information
- simple return-policy questions
- straightforward account guidance
- simple payment troubleshooting
- common technical troubleshooting with a clear known procedure

Escalation should be based on the actual risk and required action,
not simply on the intent name.

---

# Annotation Requirements

For every golden example, record:

- customer message
- intent
- escalation decision
- escalation reason
- annotator identifier

Do not use an LLM to generate the final golden labels.

Golden labels must be created or verified by humans.

---

# Unclear Cases

If a message is genuinely ambiguous:

1. Read the complete customer message.

2. Identify the customer's requested action.

3. Apply the priority/boundary rules above.

4. If still unclear, mark the example for review rather than guessing.

The final golden set should contain a mixture of:

- easy examples
- typical examples
- difficult examples
- overlapping/boundary cases
- high-risk escalation cases

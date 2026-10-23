# AI Receptionist Demo

End-to-end pipeline to build a free-tier Botpress chatbot demo trained on a real local business's public website.

## What it demonstrates
A local-business Q&A workflow grounded in a business's published information, with explicit safety boundaries rather than invented answers.

## Current state
The offline reference demo is implemented and tested. A hosted Botpress deployment is not yet configured, so this page makes no claim that a live Botpress bot is running.

## Safety behaviour
- Answers supported by the local knowledge base include source links.
- Medical advice and pricing requests are refused rather than guessed.
- Emergency phrasing redirects the visitor to contact the clinic.
- If the knowledge base has no answer, the bot says so and provides the clinic contact.

The current golden test set passes all 8 cases.

## Scope
This is a tested reference implementation, not a substitute for professional medical advice or emergency services. A hosted integration can be added after its account and API access are authorized.
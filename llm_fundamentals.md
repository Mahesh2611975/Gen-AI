# Understanding LLMs (Large Language Models)

A detailed, ground-up explanation of what an LLM is, how it generates text, and what it actually means to say it "knows" something.

## Table of Contents

1. [What is an LLM?](#1-what-is-an-llm)
2. [What Does "Large" Mean?](#2-what-does-large-mean)
3. [What is a Language Model?](#3-what-is-a-language-model)
4. [What is a Token?](#4-what-is-a-token)
5. [The Full Prediction Process](#5-the-full-prediction-process)
6. [How Does It Produce an Entire Answer?](#6-how-does-it-produce-an-entire-answer)
7. [If It Only Predicts the Next Token, How Can It Know Things?](#7-if-it-only-predicts-the-next-token-how-can-it-know-things)
8. [What Does "Learned Statistical Patterns" Actually Mean?](#8-what-does-learned-statistical-patterns-actually-mean)
9. [A Useful Mental Model](#9-a-useful-mental-model)
10. [What Does "No Database of Facts" Mean?](#10-what-does-no-database-of-facts-mean)
11. [Does That Mean an LLM Doesn't "Know" Anything?](#11-does-that-mean-an-llm-doesnt-know-anything)
12. [Why Can It Generate Code?](#12-why-can-it-generate-code)
13. [Why Does It Seem Like It's "Thinking"?](#13-why-does-it-seem-like-its-thinking)
14. [An Important Correction to the Original Definition](#14-an-important-correction-to-the-original-definition)
15. [The Whole Concept in One Example](#15-the-whole-concept-in-one-example)
16. [The Simplest Mental Model](#16-the-simplest-mental-model)
17. [Final Takeaways](#17-final-takeaways)

---

## 1. What is an LLM?

**LLM** stands for **Large Language Model**.

An LLM is a neural network that has been trained on a huge amount of text so that it learns patterns in language and can predict what token should come next.

The key idea:

> Given the text so far, predict the most appropriate next token.

Then it does that again, and again, and again — one token at a time — until a full response has been produced.

---

## 2. What Does "Large" Mean?

"Large" mainly refers to two things: the size of the model itself, and the amount of data and compute used to train it.

- An LLM can have **billions of parameters**.
- Parameters are numbers inside the neural network that get adjusted during training so the model's predictions improve over time.
- The parameters are what allow the model to capture complicated, nuanced patterns in language.

```
LLM
│
├── Neural network
│
├── Billions of parameters
│
└── Trained on huge amounts of data
```

---

## 3. What is a Language Model?

A language model is a model that learns the probability of what comes next in a sequence of text.

Example:

```
I am going to eat ...

pizza      → high probability
food       → high probability
lunch      → high probability
car        → very low probability
```

The model chooses a likely next token. Suppose it chooses `pizza`. The input now becomes:

```
I am going to eat pizza ...
```

It predicts again. Suppose it chooses `tonight`:

```
I am going to eat pizza tonight ...
```

And it keeps going. Generation, conceptually, looks like this:

```
Input
  ↓
Predict next token
  ↓
Add token
  ↓
Predict next token
  ↓
Add token
  ↓
Predict next token
  ↓
...
```

That is the fundamental mechanism behind everything an LLM produces.

---

## 4. What is a Token?

This is a key detail. The common shorthand "predict the next word" is technically inaccurate — an LLM predicts the next **token**, not necessarily a whole word.

Text is broken into smaller pieces called tokens by a component called a **tokenizer**. A token might be a whole word, or it might be a fragment of one.

Example:

```
"playing"  →  could be represented as "play" + "ing"
```

A full sentence:

```
"I love programming."
```

might be tokenized conceptually as:

```
["I", " love", " program", "ming", "."]
```

The exact split depends entirely on the tokenizer the specific model uses. So technically, an LLM predicts the **next token**, not necessarily the next whole word.

---

## 5. The Full Prediction Process

Suppose you give the model this input:

```
"The capital of France is"
```

The model does not retrieve a sentence from a database. Instead, it processes the input and computes probabilities over all possible next tokens. Conceptually:

```
The capital of France is

Paris      → 0.92
London     → 0.01
Berlin     → 0.01
Madrid     → 0.01
...
```

It selects a token — say, `Paris`. The sequence becomes:

```
The capital of France is Paris
```

Then it predicts again:

```
The capital of France is Paris ...

"and"       → ...
"."         → ...
"which"     → ...
```

And the cycle continues, one token at a time.

---

## 6. How Does It Produce an Entire Answer?

This is the important part to internalize: **an LLM does not generate a whole answer in one single operation.**

Suppose you ask:

```
Why is the sky blue?
```

The model generates the answer incrementally, conceptually like this:

```
Why is the sky blue?
        ↓
The
        ↓
The sky
        ↓
The sky appears
        ↓
The sky appears blue
        ↓
The sky appears blue because
        ↓
The sky appears blue because sunlight
        ↓
...
```

Eventually arriving at something like:

```
The sky appears blue because molecules
in Earth's atmosphere scatter shorter
wavelengths of sunlight more strongly...
```

The underlying loop is always the same:

```
┌──────────────┐
│  Input text  │
└──────┬───────┘
       ↓
Predict token
       ↓
Add token
       ↓
Predict token
       ↓
Add token
       ↓
Predict token
       ↓
      ...
```

---

## 7. If It Only Predicts the Next Token, How Can It Know Things?

A natural question: if the model is "just" predicting the next token, how can it correctly answer factual questions like:

```
Who wrote Hamlet?
```

with:

```
William Shakespeare
```

It's not because there's a stored record like:

```
Question: Who wrote Hamlet?
Answer: William Shakespeare
```

Instead, during training the model was exposed to enormous amounts of text — including sentences such as:

```
William Shakespeare wrote Hamlet.
```

Through repeated exposure across huge datasets, the model's parameters come to represent strong associations, such as:

```
Shakespeare ↔ Hamlet
Shakespeare ↔ plays
Shakespeare ↔ Macbeth
Shakespeare ↔ Romeo and Juliet
```

So when it encounters `"Hamlet was written by ..."`, its learned associations make `William Shakespeare` overwhelmingly the most probable next tokens.

---

## 8. What Does "Learned Statistical Patterns" Actually Mean?

This phrase is central to understanding LLMs.

Suppose during training the model repeatedly encounters sentences like:

```
Java is a programming language.
Java supports classes.
Java supports inheritance.
Java uses objects.
```

The model does **not** store these as rows in a database table. Instead, training adjusts its internal parameters so that certain patterns become strongly represented in the network.

As a result, later, when given:

```
Java supports
```

the model's internal representations strongly favor continuations related to:

```
classes
objects
inheritance
interfaces
...
```

The model has learned relationships and statistical regularities present in the training data — not stored facts in the database sense.

---

## 9. A Useful Mental Model

Think of an LLM as a very powerful pattern-learning machine:

```
Huge amount of text
        ↓
     Training
        ↓
Neural network parameters
        ↓
Learned language patterns
        ↓
New prompt
        ↓
Predict next token
        ↓
Predict next token
        ↓
Predict next token
        ↓
Generated answer
```

That is the core idea underlying everything an LLM does.

---

## 10. What Does "No Database of Facts" Mean?

A common beginner explanation says an LLM "has no database of facts inside it in the way a search engine does." This is meant to distinguish an LLM from a traditional search engine or database.

**Traditional database:**

```
Person       Country
---------------------
Shakespeare  England
Einstein     Germany
Newton       England
```

You could query it explicitly:

```sql
SELECT country
FROM people
WHERE person = 'Einstein';
```

and retrieve:

```
Germany
```

This is explicit, structured storage with direct lookup.

**LLM:**

An LLM is fundamentally different. It has a huge collection of learned numerical parameters:

```
Parameter 1 → 0.283...
Parameter 2 → -1.472...
Parameter 3 → 0.019...
...
billions/trillions of parameters
```

Those parameters encode learned patterns. There is normally no explicit table inside the model like:

```
Question → Answer
```

Instead, information is **distributed** across the network's parameters, rather than stored as discrete, queryable records.

---

## 11. Does That Mean an LLM Doesn't "Know" Anything?

This is where the word "know" needs care.

In everyday language people say:

> "The model knows Java."

But technically, that's shorthand. It means the model has learned enough patterns about Java that it can often produce useful and accurate information about Java. It is not necessarily "knowing" in exactly the same sense that a human knows something — there's no conscious understanding, just learned statistical structure that happens to produce accurate, useful outputs most of the time.

---

## 12. Why Can It Generate Code?

Exactly the same mechanism applies. Suppose you ask:

```
Write a Java method to reverse a string.
```

The model predicts tokens that form a likely valid response, one at a time:

```
public static String reverse(String str) {
```

then:

```
    return new StringBuilder(str)
```

then:

```
        .reverse()
```

and so on. It is still doing exactly one thing: **predict the next token**. The fact that the output happens to be syntactically valid code doesn't change the fundamental mechanism — the model has simply learned strong patterns for how code tokens follow one another.

---

## 13. Why Does It Seem Like It's "Thinking"?

Because the next-token prediction process, repeated many times, can produce complex, multi-step behavior that looks like reasoning. For example:

```
If A is greater than B,
and B is greater than C,
then A is greater than C.
```

The model can generate reasoning-like text because its training exposed it to enormous amounts of reasoning, mathematics, explanations, code, and logical argument. Modern models also use additional training and inference techniques (such as extended reasoning steps) that make this behavior substantially stronger and more reliable.

But underneath all of this, the fundamental output mechanism remains the same: **token-by-token generation**.

---

## 14. An Important Correction to the Original Definition

The statement:

> "It has no database of facts inside it"

is a useful beginner explanation, but it should not be interpreted too literally.

- An LLM **does** contain information — encoded in its parameters.
- After training, the model can often correctly produce statements such as `"The Earth orbits the Sun."` That information isn't retrieved from a SQL table inside the model, but it is also wrong to conclude that "the model contains no information."

A more accurate way to state it:

> An LLM doesn't store knowledge as a traditional database of explicit records. Instead, information and patterns from training are distributed across its learned parameters.

---

## 15. The Whole Concept in One Example

Let's put everything together with a full walkthrough.

**Input:**

```
What is inheritance in Java?
```

**Step 1 — Tokenization**

Your text is converted into tokens:

```
["What", " is", " inheritance", " in", " Java", "?"]
```

**Step 2 — Neural network processes the tokens**

The model processes the context using its learned parameters.

**Step 3 — Predict next token**

It calculates probabilities for possible next tokens:

```
Inheritance → high probability
Java        → ...
is          → ...
...
```

**Step 4 — Select a token**

Suppose it generates:

```
Inheritance
```

**Step 5 — Repeat**

Now it predicts what should come after:

```
Inheritance is
```

Then:

```
Inheritance is a
```

Then:

```
Inheritance is a mechanism
```

Then:

```
Inheritance is a mechanism in
```

This continues, one token at a time, until it has generated a complete explanation.

---

## 16. The Simplest Mental Model

```
LLM
               │
       ┌───────┴────────┐
       │                │
 Huge training      Neural network
     data             parameters
       │                │
       └───────┬────────┘
               ↓
        Learned patterns
               ↓
          Your prompt
               ↓
       Predict next token
               ↓
       Predict next token
               ↓
       Predict next token
               ↓
             ...
               ↓
        Complete response
```

---

## 17. Final Takeaways

When someone says:

> "An LLM is a neural network trained on huge amounts of text to predict the next token."

the key things to understand are:

- **Training** teaches the neural network patterns present in massive amounts of text.
- The **learned patterns** are encoded in its parameters, not stored as explicit records.
- When you give it a prompt, it uses those learned patterns to **predict the next token**.
- It **repeats this process** many times, token by token, to produce a complete answer.
- Saying the model "knows" something is shorthand for saying it has learned strong, reliable patterns about that topic — not that it performs a database lookup.

That is the foundation of how an LLM works.
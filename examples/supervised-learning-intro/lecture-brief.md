# Supervised Learning, Part 1: X → Y Mappings and Regression
Source: https://www.youtube.com/watch?v=sca5rQ9x1cA · DeepLearningAI (Andrew Ng), Machine Learning Specialization, Course 1, Week 1, Lesson 2 · ~7 min

## Learning objectives
- Explain supervised learning as learning an input → output (X → Y) mapping from examples that include the right answers.
- Recognise everyday applications as X → Y problems (spam filter, speech recognition, translation, ads, self-driving, visual inspection).
- Describe the train-then-predict workflow: learn from labelled (x, y) pairs, then predict y for a brand-new x.
- Read a prediction off a fitted model, and see that different models (line vs curve) give different predictions.
- Define regression as predicting a number from infinitely many possible values.

## Concept flow
What supervised learning is (X → Y from right answers) → it's everywhere (six applications) → how it works (train on pairs, predict new x) → a worked example (house prices) → choosing the model matters (line vs curve) → naming the task type (regression), with classification teased as next.

## Concepts

### 1. Supervised learning = learning X → Y from right answers  [00:17]
- **Core idea:** An algorithm learns a mapping from input X to output Y by seeing examples that include the correct label y for each x. Afterwards it predicts y from x alone.
- **Lecturer's example:** "99% of the economic value created by machine learning today" comes from this one type.
- **Common confusion:** "Supervised" doesn't mean a human watches the training; it means the data contains the right answers (labels).
- **Interactive visual:** *Labelled vs unlabelled toggle.* A small table of 6 emails (x) with a "spam / not spam" column (y). A toggle hides/shows the y column; with y hidden, the caption reads "unlabelled: nothing to learn the mapping from", and with y shown, "labelled pairs: the algorithm can learn X → Y". Insight: the labels are what make it *supervised*.
- **Slide text:** Supervised learning: learn X → Y from examples that include the right answer.

### 2. X → Y is everywhere  [01:03]
- **Core idea:** Many valuable applications are the same pattern with different X and Y.
- **Lecturer's example:** email → spam?; audio → text transcript (speech recognition); English → Spanish/Arabic/Hindi/Chinese/Japanese (machine translation); ad + user info → click? (online advertising, "probably the most lucrative"); image + radar → positions of other cars (self-driving); photo of a phone → scratch/dent/defect? (visual inspection, Landing AI).
- **Interactive visual:** *Input → output matcher.* Six input cards on the left (📧 email, 🎙 audio clip, 🇬🇧 English sentence, 🧑+📢 ad & user, 📷 road image, 📱 phone photo). Click one; an arrow animates to its output card on the right (spam?, transcript, Spanish text, will click?, car positions, defect?) and the application name appears. Insight: one pattern, many applications.
- **Slide text:** Same pattern, different X and Y.

### 3. Train, then predict on new x  [03:15]
- **Core idea:** First train the model on (x, y) pairs; then give it a brand-new x it has never seen and it produces its best guess of y.
- **Lecturer's example:** "Take a brand new input X, something that's never seen before, and try to produce the appropriate corresponding output y."
- **Interactive visual:** *Two-phase step-through.* Step 1 "Training": labelled pairs flow into a model box, one at a time. Step 2 "Model learned": the box shows a check mark. Step 3 "Prediction": an unlabelled x enters and a predicted ŷ comes out with a "?" turning into a value. Prev/Next buttons. Insight: labels are needed for training, not for prediction.
- **Slide text:** Train on (x, y) pairs → predict y for a new x.

### 4. Worked example: predicting house prices  [03:44]
- **Core idea:** Plot size (x, sq ft) against price (y, $1000s); fit a model; read off a prediction for a new house.
- **Lecturer's example:** A friend's 750 sq ft house; a straight-line fit gives about $150,000.
- **Interactive visual:** *Scatter plot + "friend's house" slider.* ~12 data points (size 500–2500 sq ft, price ~$80k–$450k). A fitted straight line. A slider moves a vertical marker along the x-axis (start at 750); the readout shows the predicted price from the line, e.g. 750 → ~$150k. Insight: a fitted model turns any new x into a predicted y.
- **Slide text:** Fit a model, then read off the prediction.

### 5. Line or curve? The model choice changes the answer  [04:39]
- **Core idea:** A straight line isn't the only option; a curve can fit better. Different models give different predictions, and later the course shows how to choose systematically.
- **Lecturer's example:** With a curve, the friend's house comes out "closer to $200,000" instead of $150,000. Ng notes it wouldn't be appropriate to pick whichever model gives your friend the best price.
- **Common confusion:** Picking the model that gives the answer you like; the choice should be made systematically, from the data.
- **Interactive visual:** *Line/curve toggle on the same data.* Same scatter as concept 4, with the marker fixed at 750 sq ft. A toggle switches between "straight line" and "curve"; the predicted price animates between ~$150k and ~$200k. Insight: same data, different model → different prediction.
- **Slide text:** Same data, different model, different prediction.

### 6. Regression = predicting a number  [06:06]
- **Core idea:** House-price prediction is regression: predicting a number from infinitely many possible values. Classification (next video) is the other major type.
- **Lecturer's example:** Prices could be $150,000, $70,000, $183,000, "or any other number in between".
- **Interactive visual:** *Number-line sampler.* A continuous price line from $0 to $500k; click anywhere and a value appears (e.g. $183,412), showing any value is possible. Next to it, a greyed "Classification: next lesson" card showing two buckets (spam / not spam) as a teaser. Insight: regression outputs are continuous.
- **Slide text:** Regression: predict a number from infinitely many possibilities.

## Check your understanding
1. **What makes learning "supervised"?** A) A human watches training B) The training data includes the correct output y for each x ✅ C) The model is small. *The labels are the supervision.*
2. **A model reads a photo of a phone and outputs "dent / no dent". What are X and Y?** X = photo, Y = defect label ✅. *Visual inspection, from the lecture.*
3. **A straight line predicts $150k for a 750 sq ft house; a curve predicts $200k. Which should you trust?** A) The higher one B) Whichever is chosen systematically from the data ✅ C) Always the line. *Ng: don't pick the model that gives the best price.*
4. **Predicting tomorrow's temperature in °C: regression or not?** Regression ✅. *It's a number from infinitely many possible values.*
5. **After training, does the model need y to make a prediction?** No ✅. *It takes x alone and outputs a guess of y.*

## Recap
- Supervised learning learns X → Y from examples with the right answers (labels).
- It powers spam filters, speech recognition, translation, ads, self-driving and visual inspection.
- Train on (x, y) pairs, then predict y for new x.
- The model you fit (line vs curve) changes the prediction; choose it systematically.
- Regression predicts a number; classification (next) predicts a category.

## Sources
- Video: https://www.youtube.com/watch?v=sca5rQ9x1cA (DeepLearningAI): the backbone; all concepts, examples and timestamps.
- Wikipedia, "Supervised learning": https://en.wikipedia.org/wiki/Supervised_learning (formal definition: training pairs (xᵢ, yᵢ), learned function g: X → Y; regression vs classification).
- Class Central review of Course 1: https://www.classcentral.com/report/?p=82310 (confirms the Week 1 structure and the Portland house-price dataset used in the course).

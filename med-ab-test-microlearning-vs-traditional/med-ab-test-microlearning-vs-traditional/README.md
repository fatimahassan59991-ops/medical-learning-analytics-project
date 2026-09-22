# Training Experiment: Short Lessons vs. One Long Class

A learning analytics project by Fatima Hassan

## Why I Built This

In another project on this GitHub, I studied a fictional medical school's training data and found something interesting. Long behavioral science and psychiatry courses, the kind you sit through in one long session, had much lower completion rates than short lessons covering the same kind of material. That was a strong pattern, but a pattern in existing data can only ever suggest a cause. It cannot prove one. Maybe something else about those particular courses explained the difference.

So I ran a real experiment to actually answer the question. I took one course, kept the content exactly the same, and randomly assigned medical students to either the traditional format or a short lesson format. If the format itself is really the cause, then the two randomly chosen groups should end up with different results. And because the assignment was random, format is the only real difference between them.

As with the other projects here, every student and every record is made up. No real medical school or person's information was used.

## The Experiment

I imagined 600 fictional medical students, split randomly into two equal groups, all taking the same new required course called Suicide Risk Assessment and Safety Planning. This is a skill medical schools are required to teach, and it is exactly the kind of serious material where actually remembering it matters far more than just clicking through it.

One group, the Control group, took the traditional version: one 3 hour lesson, completed in a single sitting.

The other group, the Treatment group, took the exact same material broken into six shorter 30 minute lessons, spread out over two weeks, with a short check after each one.

I split students into these two groups separately within each teaching campus, so both groups ended up with a nearly identical mix of students from each campus. That left 300 students in each group. Before the training even started, I checked whether the two groups already knew different amounts about the material. They did not, which tells me the random split worked the way it was supposed to, and any difference that shows up afterward can be credited to the training format itself, not to one group simply starting out ahead.

## What I Found

The results were clear, and they confirmed the pattern I first noticed in the earlier project.

Students in the short lesson group finished the course at a much higher rate, 93.3 percent, compared to only 67.7 percent in the traditional group. That is a difference of nearly 26 percentage points, and it is far too large to be explained by chance. Among the students who did finish, the short lesson group also scored higher on the test given after training, and they rated their satisfaction with the course much higher too, close to the top of the scale compared to the middle for the traditional group.

One honest detail worth mentioning: students in the short lesson group took longer in total calendar days to finish, since their lessons were deliberately spread out over two weeks instead of done all at once. So the short lesson format did not win on absolutely every measure. It traded a few extra days for a much better chance that students actually finish the course and remember what they learned, which matters a great deal for a skill they may one day need with a real patient.

## How I Built and Analyzed It

I generated the experiment data using Python, simulating what a real study like this would look like: students randomly split within each campus, with results that reflect a genuine training effect layered on top of normal differences between individual students, not identical numbers copied into two groups.

For the analysis, I used simple statistical comparisons matched to each type of result, checking whether the difference in completion rates, test scores, and satisfaction ratings between the two groups was big enough to be a real effect and not just noise. The docs folder has the full write up of how the experiment was designed, including how I decided how many students to include before running it, and the scripts folder has the full analysis with every number mentioned above calculated directly from the data.

## A Quick Tour of the Project

The data folder has the results of the experiment, one row per student, showing which group they were in, their scores before and after training, whether they finished, how satisfied they were, and more, along with a database file with the same information already loaded.

The sql folder has queries that calculate the group level numbers directly, including completion rates, average scores, and a check that both groups had a similar mix of students from each campus.

The scripts folder has the Python code. generate_data.py creates the simulated experiment, and analyze.py runs the analysis and produces five charts, including one that summarizes both key results side by side.

The docs folder has the full write up of how the experiment was planned: the question being tested, how students were assigned to groups, how many students were needed, and how success was defined, written the way I would document it before actually running a real experiment.

## Try It Yourself

```bash
pip install -r requirements.txt
python3 scripts/analyze.py
```

This prints the full analysis and regenerates the five charts.

## Related Projects

This is the second of three related projects on my GitHub. The first is Medical Student Behavioral Health Training Effectiveness and Learning Analytics, which is the original finding that led to this experiment. This project is the actual proof. The third project is a full redesign of the flagged course, rebuilt from the ground up using proven instructional design methods.

## Putting This on GitHub

This folder is already set up as a git project. To publish it under your own GitHub account, run these three commands:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

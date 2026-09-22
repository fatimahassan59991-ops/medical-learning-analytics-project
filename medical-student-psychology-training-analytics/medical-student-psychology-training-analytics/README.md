# Medical Student Behavioral Health Training: Effectiveness & Learning Analytics

A learning analytics project by Fatima Hassan

## Why I Built This

Every medical school has to teach behavioral science and psychiatry skills, things like how to interview a patient, how to recognize depression and suicide risk, and how to talk to someone who has been through trauma. But teaching a subject and students actually learning it are two different things. Do students finish the training? Do they remember it later? And if not, why not?

As a Learning Experience Designer, I have seen firsthand how much better training gets when the redesign is guided by real numbers instead of a guess. In one program I improved this way, the number of people who finished the course went from about 58 percent up to 91 percent.

For this project, I wanted to apply that same thinking to a topic that every medical school deals with: required behavioral health training for students who are already busy with classes and hospital rotations. So I built a full, realistic training dataset for a made up medical school and studied it the same way I would study a real one, looking for patterns that explain what is going wrong and what could fix it.

I want to be upfront that everything here is invented. Every student, every campus, and every training record was created by me. No real medical school, student, or patient information was used anywhere in this project. I built the whole dataset myself so that I could share this work publicly with zero privacy concerns.

## What I Built

I created a made up medical school called Meridian School of Medicine, with five teaching campuses and four class years (first year through fourth year students, sometimes labeled M1 through M4). There are 750 students in total. Each one is enrolled in five required Behavioral Science and Psychiatry courses, the kind of psychiatric interviewing and mental health training every medical school requires, plus one to three optional courses on related topics like motivational interviewing and physician wellness.

Altogether that adds up to about 5,200 training records. Each record includes the student's campus, the course and how it was delivered, a score from before and after the training, whether the student finished it, how long it took, how many tries it took to pass the quiz, and how satisfied the student said they were.

I wrote SQL queries to answer specific questions about the data, used Python to calculate the important numbers and build charts, and set everything up so it could also be loaded straight into Power BI to build a live dashboard.

## What the Data Shows

Overall, students finished their required training about 80 percent of the time. But that single number hides the real story.

The three longest courses, all delivered as one long digital workbook you sit through in one go, covering psychiatric interviewing, depression and suicide risk, and trauma informed care, had the worst completion rates of anything in the whole curriculum. The flagship course, Psychiatric Interviewing and Mental Status Examination, was completed by only 58.9 percent of students, the lowest of any course they were assigned.

Meanwhile, two short courses covering very similar behavioral health material, but delivered as quick, game like microlearning lessons, were completed by 96 percent or more of students, and those students also learned far more from them.

It was not about which campus a student attended. Completion rates were nearly identical across all five teaching campuses, within about 6 points of each other, so "one campus just does not care" is not the explanation. The real pattern lines up with how long and how the course was delivered. Long, sit down, one sitting courses perform worse across the board, both in whether students finish them and in how much they actually remember, which lines up with what research on attention and mental effort would predict, especially for students already juggling clinical rotations and coursework.

## How I Built It

This project uses the same core toolkit I bring to every learning and people analytics project.

I used SQL to query the data directly, comparing completion rates by course and by format, and specifically isolating course length as the real driver within the Behavioral Science and Psychiatry courses, while also checking for trends across campuses.

I used Python, with the pandas and matplotlib libraries, to process the data, calculate summary statistics, and generate clean, easy to read charts.

I stored everything in a SQLite database so the whole project can be explored using any standard SQL tool, or connected directly into Power BI to build a live dashboard.

## A Quick Tour of the Project

The data folder holds the dataset itself. It includes students.csv, courses.csv, and training_records.csv as separate tables you can practice joining together with SQL, plus training_data.csv, a single flat file that already has every column combined for quick analysis in Excel or Power BI. training.db is a SQLite database with everything already loaded, including a training_data view that does the joining work for you automatically.

The sql folder has 10 queries I wrote against this data, covering completion rate by course and by format, the comparison between long and short Behavioral Science and Psychiatry courses, campus by campus breakdowns, satisfaction by completion status, and more.

The scripts folder has the Python code. generate_data.py builds the fictional dataset from scratch, and analyze.py reads the data, prints the key numbers, and produces the five charts saved in the charts folder.

## Try It Yourself

The CSV files in the data folder open directly in Excel, Google Sheets, or Power BI, no setup needed. To run the Python analysis yourself, use these two commands:

```bash
pip install -r requirements.txt
python3 scripts/analyze.py
```

This prints the key numbers and regenerates the five charts in the charts folder.

## Using This in Power BI

First, open Power BI Desktop and go to Get Data, then More, then Database, then SQLite database (you may need to turn on the SQLite connector once, under Options and then Preview features, if it is not already on).

Next, point it at data/training.db and load the training_data view. It is already a single flat table, so there are no relationships to build.

For visuals, a good starting point is a card showing the overall completion rate, a bar chart of completion rate by course, a bar chart of learning gain by course, and a campus comparison to show that campus is not the real driver.

## Regenerating the Dataset

Everything is controlled by settings near the top of scripts/generate_data.py, including the number of students, the campuses, the course catalog, and the patterns built into the simulation. Change a value and rerun the script to get a new dataset. It will always come out the same way for the same settings, because it uses a fixed random seed, so the results are easy to reproduce.

## Related Projects

This is the first of three related projects on my GitHub, all showing the same learning analytics and instructional design skills applied to medical education and behavioral health training. This one covers the data, the analysis, and the dashboard. The second is an experiment comparing short game like microlearning against traditional one sitting instruction. The third is a full redesign of the flagged Psychiatric Interviewing and Mental Status Examination course, including a storyboard, an assessment plan, and a working interactive prototype you can click through.

## Putting This on GitHub

This folder is already set up as a git project. To publish it under your own GitHub account, run these three commands:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

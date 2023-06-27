# Association Rules

## Setting Up the Project

- Using python 3.7.x
- python3.7 -m venv "env"
- source env/bin/activate

## Running Project on the Cloud
- pip3 install numpy
- pip3 install pandas

## Run
- python3 main.py dataset.csv 0.01 0.5
- python3 main.py INTEGRATED-DATASET.csv 0.01 0.5

## Data

**Dataset Used**: [Popular Baby Names](https://data.cityofnewyork.us/Health/Popular-Baby-Names/25th-nujf)

### Dataset Modification Procedure

The original dataset contained *49.5K* rows of data, where each row described details about a popular baby name. There were 6 columns:

1. **year of birth**
2. **gender**
3. **ethnicity** (Mother's Ethnicity)
4. **child's first name**
5. **count** (Number of babies with this name)
6. **rank** (Frequency of baby names in descending order)

## Our modifications:

We used NumPy and Pandas to clean up the Popular_Baby_Name.csv file downloaded from the website.

Our changes can be found in INTEGRATED-DATASET.csv

1. Reduce data set: We noticed that the dataset contained many duplicate rows, which were completely unnecessary, so we removed those rows first. We used pandas to do so.

![Duplicates](/images/cleaning_duplicates.png)

2. Since our dataset was still so large, we need to reduce the number of rows further. We removed all rows in which the rank of the name was less than 50

3. Iterate through all the rows:
    1. Lowercase the name
    2. Lowercase the gender
    3. Lowercase the ethnicity
    4. Consolidate all ethnicities ('asian and paci' --> 'asian and pacific islander'), 
        - white non hisp -> white non hispanic
        - asian and paci -> asian and pacific islander
        - black non hisp -> black non hispanic

4. Drop the rank column: this didn’t add any value to our association rules

## Why We Chose this Data Set

We thought it would be interesting to see if there are names in particular that were popular for a given year, race, or age and how categories can be associated with each other unexpectedly.

## Internal Design on the Project

After cleaning the data set, we implemented the a-priori algorithm from Agrawal and Srikant paper in VLDB 1994. We iterated through each row in our INTEGRATED-DATASET.csv file, tallying up the number of rows, which we later used to calculate the support. In our dataset, each row does not correspond to a particular baby, but a unique (year, gender, ethnicity, name) combination. Each row is associated with a count for that combination. Because the rows are essentially collapsed, we used the count column to sum up the total number of rows for that candidate itemset.

We then performed the first pass to determine the large 1-items. We counted the number of times each item appeared in the data set and then calculated the support by dividing the count for this item by the total number of rows. If the support was greater than min_sup, we added the {item: support} pair to “L”, a list of sets that keeps track of all large item sets.

We then entered the loop for the apriori algorithm. This portion references apriori_gen, a method that uses SQL to generate candidate itemsets of size k. Here, we look at each possible size k elements, which maxes at k=4 because we have only 4 columns of meaningful information.

For k = 2, for example, we enumerate over each large itemset calculated in the first pass for k = 1. We insert each item into L1, which is then used in another SQL query. This second query inserts items into C2 in order to create new candidate pairs by appending one new item to each tuple. For k = 2, we do not perform a pruning step because L_1 contains size-1 items that have min_support. However, for k > 2, we prune the candidates by checking if a subset of them is not in L_(k-1). We remove such candidates from our C3 table.

Back in the main function, we iterate over each candidate in Ck and tally its count. We calculate the support and populate the list L[k] with the {item: support} pair if it has min_support.

Once we have the complete list L, containing all large itemsets of each size k, We get associations by making all possible combinations for the itemset and calculating the confidence. This is equivalent to the support of the itemset divided by the support of the LHS.

We then output all the large itemsets with minimum support and all the associations with minimum support and confidence.

## Command line specification

python3 main.py INTEGRATED-DATASET.csv 0.001 0.5

The results are interesting because they show which names are tied to particular genders, and other combinations:
- (year, race) → (gender)
- (gender) → (year)
- (name, gender) → (ethnicity)
- (name) → (ethnicity)

**Example:** (justin, male) -> (hispanic) conf: 54.08% supp: 0.31%
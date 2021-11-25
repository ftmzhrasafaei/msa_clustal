# MSA Clustal
Multiple Sequence Alignment using clustal model
For sequence alignment, I used global alignment. I also created a guide tree based on Neighbor-Joining method for sequence selection.
## Algorithm:
- 1 - Create a guide tree
- 2 - select 2 node of the tree for global alignment
- 3 - add the consensus of the two nodes to the tree. (for two letters with equal occurrence, I chose based on the alphabetical order)
- 4 - repeat step 2 , 3 until there is only one node.
* There is a function named "global_align" which produce the score of global alignment using these parameters: match = 1, mismatch = -1, gap = -2

## Input
line 1: n: number of sequences
line 2, ..., n + 1: sequences

## Output
line 1, ..., n: MSA
line n + 1: score of MSA

### Example
![image](https://user-images.githubusercontent.com/47606879/143396257-044dca89-34b5-4dd3-8262-8649bc4a9575.png)




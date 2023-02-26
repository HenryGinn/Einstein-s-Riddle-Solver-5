# Einstein's Riddle Solver V5
Formulating general Einstein's riddle type problems as binary integer programming problems

**Table of Contents**

1. [What Are Einstein's Riddle Type Problems?](#what-are-einsteins-riddle-type-problems)
1. [Terminology](#terminology)
1. [Formulation Overview](#formulation-overview)
1. [Consistency Constraints](#consistency-constraints)
1. [Choice of Profit Function](#choice-of-profit-function)
1. [Types of Clue and their Constraints](#types-of-clue-and-their-constraints)
1. [Well Posedness and Finding Multiple Solutions](#well-posedness-and-finding-multiple-solutions)

---

## What Are Einstein's Riddle Type Problems?

Einstein's riddle is a puzzle where there are 5 people with different nationality, house colour, house position, favourite drink, brand of cigarette, and pet. Information is given about how each of these characteristics are related with the following clues:

- The Brit lives in the red house
- The Swede keeps dogs as pets
- The Dane drinks tea
- The green house is on the left of the white house
- The green homeowner drinks coffee
- The person who smokes Pall Mall rears birds
- The owner of the yellow house smokes Dunhill
- The man living in the center house drinks milk
- The Norwegian lives in the first house
- The man who smokes Blend lives next to the one who keeps cats
- The man who keeps horses lives next to the man who smokes Dunhill
- The owner who smokes Bluemaster drinks beer
- The German smokes Prince
- The Norwegian lives next to the blue house
- The man who smokes Blend has a neighbor who drinks water
  
The goal of the riddle is to determine who owns the fish. The class of problems we are interested in will have $n$ people with $m$ characteristics where n and m are in the single digit range, and the goal will be to find all information about the system. This can be represented in an $n$ by $m$ table.

---

## Terminology

### Entity Names

- Element: the things that have the various properties. In Einstein's riddle these correspond to the 5 people
- Characteristic: the various properties that an element can have. In Einstein's riddle these are house colour, number, pet, etc
- Property: an option for a characteristic that an element could have. In Einstein's riddle, "red house" is a property of the Brit
- Family: the collection of properties that an element could have as a characteristic. For example, the family of pets is dog, cat, bird, horse, and fish.

### Problem Size

- $n$: the number of elements
- $m$: the number of characteristics

### Variables and Constraints

- We denote a variable the corresponds to two characteristics by writing $x_{\text{characteristic 1, characteristic 2}}$, for example, $x_{\text{Brit, milk}}$
- Grid variable: a variable that corresponds to a point in the grid. These are the variables which will be read off to form the solution.
- Supplementary variable: these are used to help formulate constraints, but their value is not important in the solution. An example would the variables used in big M constraints.
- Big M constraints: variables used to enforce a choice of constraints. For more information see the section [Types of Clues and Their Constraints](#types-of-clue-and-their-constraints)
- Feasible region: the set of points that are satisfied by all the constraints. As our constraints are linear this will be a polytope, and in our case will also be bounded.

---

## Formulation Overview

Each pair of characteristics has a corresponding n by n grid. We assign either a 0 or a 1 to each square in the grid to signify whether the row and column match or not. For example, if we are considering nationality and favourite drink and the Brit drinks milk, there would be a 1 in the cell corresponding to Brit and milk. The complete table will have n ones where there is only a single one in each row and column. We refer to the problem of placing ones in a grid in this manner as the rook problem for that pair of characteristics as if the 1s were rooks on a chessboard, then we are looking for configurations where none of the rooks attack each other. The entire problem can be realised as $\frac{1}{2} m(m-1)$ interconnected rook problems.

For each cell we associate with it a non-negative variable (in the end this variable will be either a 0 or a 1). The constraints of each rook problem can be imposed easily with the constraints restricting the sum of each row and the sum of each column to be less than or equal to 1. We call these rook constraints and there are $nm(m-1)$ of them: for Einstein's riddle this gives 150.

There are 4 main types of constraint:

1. Rook constraints
1. Consistency constraints
1. Clue constraints
1. Big M constraints

Here we have covered rook constraints, and consistency constraints are covered in the next section. Big M constraints are used to allow a choice of which constraints to hold, and details of them and clue constraints are given in the section [Types of Clues and Their Constraints](#types-of-clue-and-their-constraints). All our constraints will be formulated as weak inequalities. Due to the nature of the quadratic programming algorithm we use to solve this problem, we must have the origin as a feasible point. This will change how we implement some constraints, and it also means we cannot impose equality as easily. This will not be an issue however as in our case we will be able to implicitely enforce equalities via our profit function by making it always better for equality of a constraint to hold.

---

## Consistency Constraints

We need to ensure each rook problems are consistent with each other: if the Brit drinks milk and the person who drinks milk lives in the centre house, then the Brit must live in the centre house. For every pair of points that are not in the same family we need a constraint to rule out situations that make the rook problems inconsistent. We rephrase our example by saying that if the Brit drinks milk and the person who drinks milk lives in the centre house, then the Brit cannot live in any house but the centre house, and the centre house cannot be lived in by anyone but the Brit. There are 3 pairs being considered here. In each case they can either match or not match, which gives $2^3 = 8$ possibilities. We label these with a capital letter if the corresponding characteristics match, and a lowercase if they do not. We list the 3 pairs in our example below. Without loss of generality we can extend our following logic to all pairs of families and problems of other sizes as our arguments will be independent of the number of elements and factors.

<ol type="A">
  <li>Nationality and drink</li>
  <li>Nationality and house order</li>
  <li>Drink and house order</li>
</ol>

If the Brit is not the person who drinks milk for example, we know that in an optimal solution where the constraints of each rook problem are satisfied, then some non-Brit will drink milk and the Brit will drink something other than milk. This means that in the nationality and milk rook problem, the variables in the milk row (not including the Brit) and the variables in Brit row (not including milk) will sum to 2. As we know the Brit and the milk drinker are not the same person, only one of these can live in the centre house. This means the Brit and centre house variable and the milk and centre house variable must sum to at most 1. We can combine these into the following constraints. A case is consistent if and only if 0, 1, or all 3 of A, B, and C match, or equivalently, a case is inconsistent if and only if exactly 2 of A, B, and C match. This combined with the above motivates the following constraints, where each rule out one of the cases aBC, AbC, or ABc. We call these consistency constraints

$$\text{aBC}: 2x_{\text{Brit, centre house}} + 2x_{\text{milk, centre house}} + \sum_{\text{nationality} \ne \text{Brit}} x_{\text{nationality, milk}} + \sum_{\text{drink} \ne \text{milk}} x_{\text{Brit, drink}} \le 4$$
$$\text{AbC}: 2x_{\text{milk, centre house}} + 2x_{\text{Brit, milk}} + \sum_{\text{house order} \ne \text{centre house}} x_{\text{Brit, house order}} + \sum_{\text{nationality} \ne \text{Brit}} x_{\text{nationality, centre house}} \le 4$$
$$\text{ABc}: 2x_{\text{Brit, milk}} + 2x_{\text{Brit, centre house}} + \sum_{\text{drink} \ne \text{milk}} x_{\text{drink, centre house}} + \sum_{\text{house order} \ne \text{centre house}} x_{\text{milk, house order}} \le 4$$

We need all consistent cases to pass, and all non-consistent cases to fail. As we want the optimum of our system to be our solution, and we only care about the solution being consistent, we can assume that as many of the variables are 1s as possible. For us this means that each individual rook problem of size n has n rooks. If we are in the case abc, the first two terms in our constraints will be 0 and the last two terms will each be 1. This gives us $0 + 0 + 1 + 1 = 2$ which is less than 4 and our constraints are satisfied. If we are in the cases Abc, aBc, or abC, then one of the first two terms will be 2, the other will be 0, and the last two terms will either be both 1 or both 0. For example in each of those three cases, the first constraint reads as $0 + 0 + 0 \le 4$, $2 + 0 + 2 \le 4$, and $0 + 2 + 2 \le 4$ respectively. In the cases aBC, AbC, and ABc, exactly two families match and we need at least one of the constraints to fail. In the case aBC, all of the terms in the first constraint are equal to 2, and we get a total of 6. We have a similar situation with AbC and ABc and the other two constraints. Finally in the case ABC, the first two terms in each constraint are both 2 and the last two terms are 0 so our constraints are all satisfied.

For a given triple of families, we need $3n^3$ constraints as we need constraints for every combination of characteristics for each family. If there are $m$ families then we have ${m \choose 3} = \frac{1}{6} m(m-1)(m-2)$ triples of families which gives a total of $\frac{1}{2} n^3 m(m-1)(m-2)$ constraints. For Einstein's riddle this is 7500. We note that some of these constraints are unnecessary, and only $\frac{1}{2} (n-1)^3 m(m-1)(m-2)$ constraints are needed which would approximately half the number of constraints needed for Einstein's riddle to 3840. If there are $n$ elements, it is impossible for $n-1$ of them to be consistent and only one of them inconsistent - an inconsistency affects at least two elements.

For example, if the Brit drinks milk, the milk drinker lives in the centre house, and the person who lives in the centre house is not the Brit is an inconsistency. If the person who lives in the centre house is not the Brit, that must mean they are some other nationality, let's say the German. As the German lives in the centre house, they must be the milk drinker, but we know they are not the milk-drinker. In this case, the Brit, milk-drinker, and centre house inconsistency implied a German, milk-drinker, and centre house inconsistency. This means we only need to check for one of these inconsistencies. An intuition for this can be seen by starting with a consistent problem and flipping a pair of rows or a pair of columns in one of the rook problems. We see that this will cause in two of the elements. This means that when forming inconsistency constraints, we only need to make them for $n-1$ of the elements instead of $n$, as any inconsistency in an ignored element will co-occur with an inconsistency in an element that is checked.

---

## Choice of Profit Function

We want all our variables to be 0 or 1, but we do not explicitely impose any integrality constraints. The variables in the optimal solutions will be guaranteed to be integers by the combination of the geometry of the feasible region and the geometry of our profit function.

We can place an upper bound on how many ones can be put into our grid due to the rook constraints. This is because in each rook problem, each row can only have a single one in it, and there are $\frac{1}{2} nm(m-1)$ rows. In a problem where at least one solution exists, any such solution will reach this upper bound. The valid solutions to our programming problem are those where the variables are 0 or 1, and we have maximised the number of ones. We choose our profit function so that the only feasible points where our profit function are maximised are integers.

We demonstrate the problem on the small example of placing as many rooks on a 2 by 1 chess board where no rook attacks any other rooks. As described earlier, we can track the number of rooks in each cell with non-negative variables which we will call $x$ and $y$, where 0 and 1 respectively describe rook not present and rook present in each cell. We have one rook constraint which is $x + y \le 1$, and when plotting this on a set of axes, we see the feasible region is a right-angled isosceles triangle. Each point within this triangle describes a configuration of rooks on the board, but obviously only $(0, 0)$, $(1, 0)$, and $(0, 1)$ correspond to real configurations. Naively we might choose to place the rooks on the board by maximising the linear profit function $P = x + y$. $(1, 0)$ and $(0, 1)$ are indeed maximers of this function within the feasible region, but any point on the line $x + y = 1$ with $0 < x, y < 1$ is also a maximer of this function. These solutions are unphysical as it is impossible to have a fractional number of rooks in a cell.

Adding a bias towards one side and choosing a function such as $P = 1.1x + y$ would fix the issue in this case, but we do not want a bias and we choose a symmetrical profit function. Instead we use the fact that for $0 < x < 1$ we have $x^2 < x$, and for $x \ge 1$ we have $x^2 \ge 1$. This motivates the choice $P = x^2 + y^2$, as numbers closer to 1 will be prioritsed. If we substitue $y = 1 - x$ into $P$ we get $P = x^2 + (1 - x)^2 = 2x^2 - 2x + 1$, and solving for $P \ge 1$ gives $x(x-1) \ge 0$. The only solutions within the range $0 \le x \le 1$ are $x = 0$ and $x = 1$, and these correspond to the points $(1, 0)$ and $(0, 1)$ respectively. Looking at $x^2 + y^2 = 1$ on a plot with the feasible region marked shows why this profit function is a good choice for this problem.

In general any profit function where it's hessian has non-negative eignevalues which are not all equal to 0 will work. Geometrically this means that the surface of the profit function will lie stricly "above" any secant hyperplane (going further away from the origin) instead of below in the interior of the loop defined by the intersection of the hyerplane and the profit function. As all our constraints are linear combinations of variables bounded by a constant, they describe the half space on one side of a hyperplane (in our case this will be the side containing the origin, or "beneath the hyperplane"). If we consider an integer optimal point over a polytope domain, then we see that we do not get the same issue as with the linear profit function. Choosing any direction and following the surface of the profit function, we immediately become unfeasible as we will be going into the interior of a loop defined by the intersection of the profit function and one of the hyperplanes, and this means we will be above the hyperplane, and so will not satisfy that constraint.

---

## Types of Clue and their Constraints

In this section we will cover the following types of clue:

1. [Non-matching of properties](#1-non-matching-of-properties)
1. [Matching of properties](#2-matching-of-properties)
1. [Choice of multiple clues](#3-choice-of-multiple-clues)
1. [Quantative relations](#4-quantitative-relations)

### 1: Non-Matching of Properties

This is the simplest type of clue, and an example of this would be "The Brit does not live in the blue house". We can enforce this immediately by imposing the constraint $x_{\text{Brit, blue}} \le 0$.

### 2: Matching of Properties

This type of constraint is also very simple and most of the constraints in Einstein's riddle take this form. An example would be "The Brit lives in the red house". As we need the origin to be a feasible point, we cannot simply impose the constraint that $x_{\text{Brit, red}} \ge 1$, but we can take advantage of the rook constraints and the fact that in the optimal solution, all rook problems will be at capacity in order to encode this information. We insist that all other variables in the Brit row/column of the nationality and house colour rook problem sum to at most 0. Equivalently we could also use the constraint that all other variables in the red column/row of nationality and house colour rook problem sum to at most 0. Yet another alternative will be to insist that the other variables in both the rows and the columns sum to at most 0. All of these describe a different feasible region, but the set of optimal points consistent with the rook and consistency constraints will be the same.

### 3: Choice of Multiple Clues

Multiple clues can be combined with logical OR. An example of this would be "Either the Brit drinks milk or the fish owner lives in the green house". It is possible for both of these to be true at once, but if the clue is given as an exclusive OR and only one of the options is allowed, then further constraints would be needed to disallow that possibility. Suppose two clues can be encoded with the constraints $A_1 x \le b_1$ and $A_2 x \le b_2$ respectively. If we have constant vectors $M_1$ and $M_2$ such that $A_1 x \le M_1$ and $A_2 x \le M_2$ always hold for any choice of x then we can use this to control when each constraint is turned on. We introduce variables $y_1 and y_2$ with the constraint that $y_1 + y_2 \le 1$, and use these to control the constraints - $(y_1, y_2) = (1, 0)$ will mean that $A_1 x \le b_1$ will hold and $(y_1, y_2) = (0, 1)$ will mean that $A_2 x \le b_2$ will hold. Our aim is to allow the right hand side of the inequalities in the constraints to change - if the right hand side is suffiently large enough for the constraint to always hold, that constraint does not actually constrain the problem at all, so it will have been effectively turned off. This motivates considering the constraints $A_1 x \le b_1 + M_1 y_2$ and $A_2 x \le b_2 + M_2 y_1$. Here we see that when $y_1 = 0$ the first constraint is as it was before, and so it will be active, and similarly if $y_2 = 0$.

To avoid both constraints being active, we would need $y_2 = 1$ if $y_1 = 0$ and vice versa. This turns out not to be a problem however, as the maximum profit cannot be increased by adding constraints, so by the nature of optimisation, the least constraining sitution will naturally be found. Another potential problem is $y_1$ and $y_2$ not being integers, as this means both constraints are not imposed. This can be remedied by adding $y_1^2 + y_2^2$ into our profit function, and as argued earlier, this will impose that $y_1$ and $y_2$ are integers. The existence of $M_1$ and $M_2$ is seen by the fact that the maximum each variable can be is 1, there are a finite number of variables, and the coefficients in the constraints are also finite. Given a linear combination $c^T x$, it is very easy to find an upper bound - if $c_i < 0$ then set $x_i = 0$, and if $c_i \ge 0$ set $x_i = 1$. Computing $c^T x + 1$ with this choice of $x$ will give a valid upper bound, and these can be combined to find the M vector. This is called a big M constraint, and we call the variables $y_1$ and $y_2$ big M variables. We also note that if there are $n$ constraints then we have $n$ big M variables and each constraint will look like $A_i x \le b_i + M_i (y_1 + \dots + y_{i-1} + y_{i+1} + \dots + y_n)$. It is also possible that a constraint that has not been imposed will happen to hold anyway.

### 4: Quantitative Relations

Some variables such as house order and age are quantitatve, and so there are more ways to describe restrictions. An example of this would be saying one of the elements is older or taller than another element, or such as in Einstein's riddle, "The man who smokes Blend lives next to the one who keeps cats".

---

## Well Posedness and Finding Multiple Solutions

If a problem has a solution then it will be in the feasible region. We also know that due to the rook constraints that the total of all the variables in the grid will be $\frac{1}{1} nm(m-1)$, and because we are maximising $x^Tx$, the profit function can only achieve $\frac{1}{2} nm(m-1)$ if all variables are 0 or 1. If an optimal point is found with the maximal profit we know that it will be a valid solution as if any variables are not 0 or 1 then the profit would be able to be increased past the upper bound for the profit. This follows from the arguments made in the "Choice of Profit Function" subsection found in the section [Choice of Profit Function](#choice-of-profit-function). A solution exists if and only if the maximum profit is $\frac{1}{2} nm(m-1)$, and if a feasible point has maximal profit then it is a valid solution.

Finding multiple solutions can be achieved through an iterative process. An optimal point is found and some grid variables will be 0 and some will be 1. We will search for different solutions by adding a constraint to remove this point from the feasible region and attempting to optimise the problem again. We can do this by choosing a constraint that adds up all the variables that are equal to 1 and insisting that the sum is bounded by $\frac{1}{2} nm(m-1) - 1$. As the sum of variables equal to 1 in this solution add to $\frac{1}{2} nm(m-1)$, the point that has just been found would not be feasible with this new constraint. We also note that we do not remove any other solutions with this constraint as the only way a solution can lie beyond this constraint hyperplane is if it is identically equal to the old solution. This follows from the rook constraints.

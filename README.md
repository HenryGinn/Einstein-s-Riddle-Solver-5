# Einstein's Riddle Solver V5

## **Table of Contents**

1. [What Are Einstein's Riddle Type Problems?](#what-are-einsteins-riddle-type-problems)
1. [Terminology](#terminology)
1. [Formulation Overview](#formulation-overview)
1. [Consistency Constraints](#consistency-constraints)
1. [Choice of Profit Function](#choice-of-profit-function)
1. [Types of Clue and their Constraints](#types-of-clue-and-their-constraints)
1. [Family Relations](#family-relations)
1. [Murder Mystery Variation](#murder-mystery-variation)
1. [Well Posedness and Finding Multiple Solutions](#well-posedness-and-finding-multiple-solutions)
1. [Program Structure and Implementation](#program-structure-and-implementation)
1. [Family Tree Construction](#family-tree-construction)
1. [Clue Structure](#clue-structure)

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
  
The goal of the riddle is to determine who owns the fish. The class of problems we are interested in will have $n$ people with $m$ characteristics where $n$ and $m$ are in the single digit range, and the goal will be to find all information about the system. This can be represented in an $n$ by $m$ table.

---

## Terminology

### Entity Names

- Element: the things that have the various properties. In Einstein's riddle these correspond to the 5 people
- Characteristic: the various properties that an element can have. In Einstein's riddle these are house colour, number, pet, etc
- Property: an option for a characteristic that an element could have. In Einstein's riddle, "red house" is a property of the Brit
- Group: the collection of properties that an element could have as a characteristic. For example, the group of pets is dog, cat, bird, horse, and fish.
- Concrete property: a property that is explicitely mentioned. "The uncle of the person who lives in the centre house" is not concrete, but "The person who lives in the centre house" is.

### Problem Size

- $n$: the number of elements
- $m$: the number of characteristics

### Variables and Constraints

- We denote a variable the corresponds to two characteristics by writing $x_{\text{characteristic 1, characteristic 2}}$, for example, $x_{\text{Brit, milk}}$
- Grid variable: a variable that corresponds to a point in the grid. These are the variables which will be read off to form the solution.
- Supplementary variable: these are used to help formulate constraints, but their value is not important in the solution. An example would the variables used in big M constraints.
- Big M constraints: variables used to enforce a choice of constraints. For more information see the section [Types of Clues and Their Constraints](#types-of-clue-and-their-constraints)
- Feasible region: the set of points that are satisfied by all the constraints. As our constraints are linear this will be a polytope, and in our case will also be bounded.
- Positive constraint: something is enforced to match
- Negative constraint: something is enforced to not match.

---

## Formulation Overview

Each pair of characteristics has a corresponding n by n grid. We assign either a 0 or a 1 to each square in the grid to signify whether the row and column match or not. For example, if we are considering nationality and favourite drink and the Brit drinks milk, there would be a 1 in the cell corresponding to Brit and milk. The complete table will have n ones where there is only a single one in each row and column. We refer to the problem of placing ones in a grid in this manner as the rook problem for that pair of characteristics as if the 1s were rooks on a chessboard, then we are looking for configurations where none of the rooks attack each other. The entire problem can be realised as ${\frac{1}{2} m(m-1)}$ interconnected rook problems.

For each cell we associate with it a non-negative variable (in the end this variable will be either a 0 or a 1). The constraints of each rook problem can be imposed easily with the constraints restricting the sum of each row and the sum of each column to be less than or equal to 1. We call these rook constraints and there are ${nm(m-1)}$ of them: for Einstein's riddle this gives 150.

There are 4 main types of constraint:

1. Rook constraints
1. Consistency constraints
1. Clue constraints
1. Big M constraints

Here we have covered rook constraints, and consistency constraints are covered in the next section. Big M constraints are used to allow a choice of which constraints to hold, and details of them and clue constraints are given in the section [Types of Clues and Their Constraints](#types-of-clue-and-their-constraints). All our constraints will be formulated as weak inequalities. Due to the nature of the quadratic programming algorithm we use to solve this problem, we must have the origin as a feasible point. This will change how we implement some constraints, and it also means we cannot impose equality as easily. This will not be an issue however as in our case we will be able to implicitely enforce equalities via our profit function by making it always better for equality of a constraint to hold.

---

## Consistency Constraints

We need to ensure each rook problems are consistent with each other: if the Brit drinks milk and the person who drinks milk lives in the centre house, then the Brit must live in the centre house. For every pair of points that are not in the same group we need a constraint to rule out situations that make the rook problems inconsistent. We rephrase our example by saying that if the Brit drinks milk and the person who drinks milk lives in the centre house, then the Brit cannot live in any house but the centre house, and the centre house cannot be lived in by anyone but the Brit. There are 3 pairs being considered here. In each case they can either match or not match, which gives $2^3 = 8$ possibilities. We label these with a capital letter if the corresponding characteristics match, and a lowercase if they do not. We list the 3 pairs in our example below. Without loss of generality we can extend our following logic to all pairs of families and problems of other sizes as our arguments will be independent of the number of elements and factors.

<ol type="A">
  <li>Nationality and drink</li>
  <li>Nationality and house order</li>
  <li>Drink and house order</li>
</ol>

If the Brit is not the person who drinks milk for example, we know that in an optimal solution where the constraints of each rook problem are satisfied, then some non-Brit will drink milk and the Brit will drink something other than milk. This means that in the nationality and milk rook problem, the variables in the milk row (not including the Brit) and the variables in Brit row (not including milk) will sum to 2. As we know the Brit and the milk drinker are not the same person, only one of these can live in the centre house. This means the Brit and centre house variable and the milk and centre house variable must sum to at most 1. We can combine these into the following constraints. A case is consistent if and only if 0, 1, or all 3 of A, B, and C match, or equivalently, a case is inconsistent if and only if exactly 2 of A, B, and C match. This combined with the above motivates the following constraints, where each rule out one of the cases aBC, AbC, or ABc. We call these consistency constraints.

$$\text{aBC}: 2x_{\text{Brit, centre house}} + 2x_{\text{milk, centre house}} + \sum_{\text{nationality} \ne \text{Brit}} x_{\text{nationality, milk}} + \sum_{\text{drink} \ne \text{milk}} x_{\text{Brit, drink}} \le 4$$

$$\text{AbC}: 2x_{\text{milk, centre house}} + 2x_{\text{Brit, milk}} + \sum_{\text{house order} \ne \text{centre house}} x_{\text{Brit, house order}} + \sum_{\text{nationality} \ne \text{Brit}} x_{\text{nationality, centre house}} \le 4$$

$$\text{ABc}: 2x_{\text{Brit, milk}} + 2x_{\text{Brit, centre house}} + \sum_{\text{drink} \ne \text{milk}} x_{\text{drink, centre house}} + \sum_{\text{house order} \ne \text{centre house}} x_{\text{milk, house order}} \le 4$$

We need all consistent cases to pass, and all non-consistent cases to fail. As we want the optimum of our system to be our solution, and we only care about the solution being consistent, we can assume that as many of the variables are 1s as possible. For us this means that each individual rook problem of size n has n rooks. If we are in the case abc, the first two terms in our constraints will be 0 and the last two terms will each be 1. This gives us ${0 + 0 + 1 + 1 = 2}$ which is less than 4 and our constraints are satisfied. If we are in the cases Abc, aBc, or abC, then one of the first two terms will be 2, the other will be 0, and the last two terms will either be both 1 or both 0. For example in each of those three cases, the first constraint reads as $0 + 0 + 0 \le 4$, $2 + 0 + 2 \le 4$, and $0 + 2 + 2 \le 4$ respectively. In the cases aBC, AbC, and ABc, exactly two families match and we need at least one of the constraints to fail. In the case aBC, all of the terms in the first constraint are equal to 2, and we get a total of 6. We have a similar situation with AbC and ABc and the other two constraints. Finally in the case ABC, the first two terms in each constraint are both 2 and the last two terms are 0 so our constraints are all satisfied.

For a given triple of families, we need $3n^3$ constraints as we need constraints for every combination of characteristics for each group. If there are $m$ families then we have ${{m \choose 3} = \frac{1}{6} m(m-1)(m-2)}$ triples of families which gives a total of ${\frac{1}{2} n^3 m(m-1)(m-2)}$ constraints. For Einstein's riddle this is 7500. We note that some of these constraints are unnecessary, and only ${\frac{1}{2} (n-1)^3 m(m-1)(m-2)}$ constraints are needed which would approximately half the number of constraints needed for Einstein's riddle to 3840. If there are $n$ elements, it is impossible for $n-1$ of them to be consistent and only one of them inconsistent - an inconsistency affects at least two elements.

For example, if the Brit drinks milk, the milk drinker lives in the centre house, and the person who lives in the centre house is not the Brit is an inconsistency. If the person who lives in the centre house is not the Brit, that must mean they are some other nationality, let's say the German. As the German lives in the centre house, they must be the milk drinker, but we know they are not the milk-drinker. In this case, the Brit, milk-drinker, and centre house inconsistency implied a German, milk-drinker, and centre house inconsistency. This means we only need to check for one of these inconsistencies. An intuition for this can be seen by starting with a consistent problem and flipping a pair of rows or a pair of columns in one of the rook problems. We see that this will cause in two of the elements. This means that when forming inconsistency constraints, we only need to make them for ${n-1}$ of the elements instead of $n$, as any inconsistency in an ignored element will co-occur with an inconsistency in an element that is checked.

---

## Choice of Profit Function

We want all our variables to be 0 or 1, but we do not explicitely impose any integrality constraints. The variables in the optimal solutions will be guaranteed to be integers by the combination of the geometry of the feasible region and the geometry of our profit function.

We can place an upper bound on how many ones can be put into our grid due to the rook constraints. This is because in each rook problem, each row can only have a single one in it, and there are ${\frac{1}{2} nm(m-1)}$ rows. In a problem where at least one solution exists, any such solution will reach this upper bound. The valid solutions to our programming problem are those where the variables are 0 or 1, and we have maximised the number of ones. We choose our profit function so that the only feasible points where our profit function are maximised are integers.

We demonstrate the problem on the small example of placing as many rooks on a 2 by 1 chess board where no rook attacks any other rooks. As described earlier, we can track the number of rooks in each cell with non-negative variables which we will call $x$ and $y$, where 0 and 1 respectively describe rook not present and rook present in each cell. We have one rook constraint which is $x + y \le 1$, and when plotting this on a set of axes, we see the feasible region is a right-angled isosceles triangle. Each point within this triangle describes a configuration of rooks on the board, but obviously only $(0, 0)$, $(1, 0)$, and $(0, 1)$ correspond to real configurations. Naively we might choose to place the rooks on the board by maximising the linear profit function $P = x + y$. $(1, 0)$ and $(0, 1)$ are indeed maximers of this function within the feasible region, but any point on the line $x + y = 1$ with $0 < x, y < 1$ is also a maximer of this function. These solutions are unphysical as it is impossible to have a fractional number of rooks in a cell.

Adding a bias towards one side and choosing a function such as $P = 1.1x + y$ would fix the issue in this case, but we do not want a bias and we choose a symmetrical profit function. Instead we use the fact that for $0 < x < 1$ we have $x^2 < x$, and for $x \ge 1$ we have $x^2 \ge 1$. This motivates the choice $P = x^2 + y^2$, as numbers closer to 1 will be prioritsed. If we substitue $y = 1 - x$ into $P$ we get ${P = x^2 + (1 - x)^2 = 2x^2 - 2x + 1}$, and solving for ${P \ge 1}$ gives ${x(x-1) \ge 0}$. The only solutions within the range ${0 \le x \le 1}$ are $x = 0$ and $x = 1$, and these correspond to the points $(1, 0)$ and $(0, 1)$ respectively. Looking at ${x^2 + y^2 = 1}$ on a plot with the feasible region marked shows why this profit function is a good choice for this problem.

In general any profit function where it's hessian has non-negative eignevalues which are not all equal to 0 will work. Geometrically this means that the surface of the profit function will lie stricly "above" any secant hyperplane (going further away from the origin) instead of below in the interior of the loop defined by the intersection of the hyerplane and the profit function. As all our constraints are linear combinations of variables bounded by a constant, they describe the half space on one side of a hyperplane (in our case this will be the side containing the origin, or "beneath the hyperplane"). If we consider an integer optimal point over a polytope domain, then we see that we do not get the same issue as with the linear profit function. Choosing any direction and following the surface of the profit function, we immediately become unfeasible as we will be going into the interior of a loop defined by the intersection of the profit function and one of the hyperplanes, and this means we will be above the hyperplane, and so will not satisfy that constraint.

---

## Types of Clue and their Constraints

In this section we will cover the following types of clue:

1. [Non-matching of properties](#1-non-matching-of-properties)
1. [Matching of properties](#2-matching-of-properties)
1. [Choice of multiple clues](#3-choice-of-multiple-clues)
1. [Quantative relations](#4-quantitative-relations)

### 1: Non-Matching of Properties

This is the simplest type of clue, and an example of this would be "The Brit does not live in the blue house". We can enforce this immediately by imposing the constraint $x_{\text{Brit, blue}} \le 0$. We will refer to this as a negative constraint because we are saying something is now allowed.

### 2: Matching of Properties

This type of constraint is also very simple and most of the constraints in Einstein's riddle take this form. An example would be "The Brit lives in the red house". As we need the origin to be a feasible point, we cannot simply impose the constraint that $x_{\text{Brit, red}} \ge 1$, but we can take advantage of the rook constraints and the fact that in the optimal solution, all rook problems will be at capacity in order to encode this information. We insist that all other variables in the Brit row/column of the nationality and house colour rook problem sum to at most 0. Equivalently we could also use the constraint that all other variables in the red column/row of nationality and house colour rook problem sum to at most 0. Yet another alternative will be to insist that the other variables in both the rows and the columns sum to at most 0. All of these describe a different feasible region, but the set of optimal points consistent with the rook and consistency constraints will be the same. We refer to this as a positive constraint because we are enforcing that a variable is non-zero.

### 3: Choice of Multiple Clues

Multiple clues can be combined with logical OR. An example of this would be "Either the Brit drinks milk or the fish owner lives in the green house". It is possible for both of these to be true at once, but if the clue is given as an exclusive OR and only one of the options is allowed, then further constraints would be needed to disallow that possibility. Suppose two clues can be encoded with the constraints ${A_1 x \le b_1}$ and ${A_2 x \le b_2}$ respectively. If we have constant vectors $M_1$ and $M_2$ such that ${A_1 x \le M_1}$ and ${A_2 x \le M_2}$ always hold for any choice of x then we can use this to control when each constraint is turned on. We introduce variables $y_1 and y_2$ with the constraint that ${y_1 + y_2 \le 1}$, and use these to control the constraints - $(y_1, y_2) = (1, 0)$ will mean that ${A_1 x \le b_1}$ will hold and $(y_1, y_2) = (0, 1)$ will mean that ${A_2 x \le b_2}$ will hold. Our aim is to allow the right hand side of the inequalities in the constraints to change - if the right hand side is suffiently large enough for the constraint to always hold, that constraint does not actually constrain the problem at all, so it will have been effectively turned off. This motivates considering the constraints ${A_1 x \le b_1 + y_2 M_1}$ and ${A_2 x \le b_2 + y_1 M_2}$. Here we see that when $y_1 = 0$ the first constraint is as it was before, and so it will be active, and similarly if $y_2 = 0$.

To avoid both constraints being active, we would need $y_2 = 1$ if $y_1 = 0$ and vice versa. This turns out not to be a problem however, as the maximum profit cannot be increased by adding constraints, so by the nature of optimisation, the least constraining sitution will naturally be found. Another potential problem is $y_1$ and $y_2$ not being integers, as this means both constraints are not imposed. This can be remedied by adding ${y_1^2 + y_2^2}$ into our profit function, and as argued earlier, this will impose that $y_1$ and $y_2$ are integers. The existence of $M_1$ and $M_2$ is seen by the fact that the maximum each variable can be is 1, there are a finite number of variables, and the coefficients in the constraints are also finite. Given a linear combination $c^T x$, it is very easy to find an upper bound: if $c_i < 0$ then set $x_i = 0$, and if $c_i \ge 0$ set $x_i = 1$. Computing $c^T x + 1$ with this choice of $x$ will give a valid upper bound, and these can be combined to find the M vector. This is called a big M constraint, and we call the variables $y_1$ and $y_2$ big M variables. We also note that if there are $n$ constraints then we have $n$ big M variables and each constraint will look like ${A_i x \le b_i + (y_1 + \dots + y_{i-1} + y_{i+1} + \dots + y_n) M_i}$. It is also possible that a constraint that has not been imposed will happen to hold anyway.

### 4: Quantitative Relations

Some variables such as house order and age are quantitatve, and so there are more ways to describe restrictions. An example of this would be saying one of the elements is older or taller than another element, or such as in Einstein's riddle, "The man who smokes Blend lives next to the one who keeps cats". We will refer to the quantitative characteristic as position to correspond with Einstein's riddle, but this could be any such quantitative characteristic. All such relations are possible to formulate as constraints by enumerating all valid states consistent with the clue, formulating a constraint that enforces each state, and then using big M constraints so that at least one of those states is enforced. We will give alternative implementations that are cleaner however.

An example of an inequality constraint would be "The green house is on the left of the white house". This could be interpreted as the green house being directly on the left of the white house, or that the green house is anywhere on the left of the white house. We will choose the latter of these options as it is weaker, and the former is dicussed next. Without loss of generality we will consider the case that X < Y where for example, "green < white" should be read as "_the position of_ green < _the position of_ white". Equivalently we can describe this as X $\ngeq$ Y, and as X $\neq$ Y is already enforced by the rook constraints, we only need X $\ngtr$ Y. There are $n$ different positions for X to be in and we have one constraint per position. For example, if X was in position 3 then it would be impossible for Y to be in positions $4, 5, \dots, n$, and vice versa. We can rule out the possibility of this happening by enforcing the constraint that the sum of those variables is bounded by 1. There are only ${n - 1}$ of these constraints.

$$ x_{\text{X, } i} + \sum_{j > i} x_{\text{Y, } j} \le 1 \iff x_{\text{X, } i} + \sum_{j = i+1}^n x_{\text{Y, } j} \le 1$$

Now we consider equality clues such as "The green house is directly on the left of the white house", or "The red house is 2 houses to the left of the white house". Suppose we have the constraint that X is directly on the right of Y and X is in position 2. This means Y has to be in position 3, which is the same as saying that Y can't be any position other than 3. We can write this as the following constraint:

$$x_{\text{X}, 2} + \sum_{\text{position} \neq 3} x_{\text{Y}, \text{position}} \le 1$$

If X is in position 2 then this forces Y to be in position 3, and if X is not in position 2, then $x_{\text{X}, 2} = 0$, so the constraint will hold automatically due to the rook constraints. There are only $n$ of these constraints, and it is easy to see how other equalities can be represented in this way, including clues such as "The man who smokes Blend lives next to the person who keeps cats" which allow an elements to be on either side of another element.

There are are the negations of the previous two types of clues. The negation of "The green house is on the left of the white house" is "The green house is not on the left of the white house", although this can be put back into the original form by rephrasing as "The green house is on the right of the white house" or "The white house is on the left of the green house". The negation of an equality constraint would be something like "The man who smokes Blend does not live next to the person who keeps cats", and this can be formulated in a similar way as the original. For each possible position of X (the man who smokes Blend in this case), we know which positions are impossible for Y (the person who keeps cats). The sum of the variables corresponding to these can be constrained to be less than or equal to one and everything follows just as before.

We close our discussion on quantitative relations by noting that even more complicated clues are possible such as, "The person who keeps horses is either 1 house to the right of the person who drinks tea, or to the left of the person who drinks tea, but not 2 houses to the left". Such clues
can be implemented using a choice of multiple clues, and the user will need to interpret the information from the clue and choose how to encode it using the built-in clue types.

---

## Family Relations

This is a special type of characteristic where the elements are members of a family. An example of a family clue would be "The uncle of the person who has a dog drinks water". There are two complications here. Firstly, relational information can apply to several elements - the brother of one person could be the uncle of niece of another person, so we brother cannot be the property of an element without a reference. The second issue is even harder to deal with, and it is the fact we do not know in advance what the family tree looks like. There is also the case where the gender may or may not be given in a clue. We will restrict ourselves to the case where all elements are related to each other, and that each relation is distinct to rule out situations such as two male siblings, but a male and female pair of siblings would be allowed.

We assign one property of one of the elements to be the reference property, and consider all possible relations to this property. For example if there were three elements, the relations would be grandchild, child 1 and 2, nibling, sibling 1 and 2, parent 1 and 2, pibling, and grandparent, where each of these has a male and female version. "Nibling" and "Pibling" are the gender-neutral terms we will use for "nieces and nephews" and "aunts and uncles" respectively. As in this case we have 3 elements, we can only have 3 of these at once, so we assign an indicator variable to each one, and insist that they sum to 3, or in general, $n$. The purpose of the reference property is to give an absolute grounding for the relations. It allows us to put labels on the elements that describe their position in the family tree, such as "grandfather".

As we are exploring all possible families relative to the reference property, we have one degree of freedom, and we use this degree to fix the reference property. To make this more concrete we consider the example of a linear family tree with no branches. If the Brit was the youngest then their relations to everyone else would be parent, grandparent, great grandparent, and great great grandparent. If they were the oldest then the relations would be child, grandchild, great grandchild, and great great grandchild. The number of possible relations can be quite large, especially as the number of elements increases, so information about the shape of the family tree should be taken advantage of. For example if one property is given as the youngest generation, that property should be set as the reference property and then only generations at that level and higher considered.

We will refer to the reference property as R, and X and Y for general properties, not necessarily different to the reference property. Our method will be to use big M constraints to cover all possible cases of how the elements with properties X and Y are related to the element with property R. Suppose we are given the clue that the daughter of the element with property X has property Y. A possible situation is that the element with property X is the brother of the element with property R, and in this case the daughter of the element with property X would be the daughter of the brother of the element with property R, making them the niece of the element with property R. Note how we only ever need to consider the rook problem with X and Y, and we do not need to look at the rook problems with X and R or Y and R. Phrasing the above without explicit reference to R, we get "If X is the brother, then the niece has Y".

We do not increase the number of dimensions of the problem by doing this as the big M variables already exist. In the above example the relevant indicator variable is ${x_{\text{X, brother}}}$, and the constraint that the indicators sum to 1 is given naturally by the existing rook constraints so we do not need any additional constraints to enforce consistency of the indicator variables. We also note that clues such as "The Brit has no siblings" can be encoded by saying that the German is not the Brit's brother, the German is not the Brit's sister, and so on for the other nationalities. This only needs to be done for one set of characteristics, and the others are implied by consistency. The constraints are in the same form as before, but with the big M constraints included (see subsection [choice of multiple clues](#3-choice-of-multiple-clues) for more details). Here we give the negative and positive version of the constraint described in the preceding paragraph. Due to the rook constraints we can use ${M_1 = 3 = M_2}$ for our big M constants.

$$x_{\text{niece, Y}} \le 0 + M_1\sum_{\text{relation} \ne \text{brother}} x_{\text{relation, X}}$$

$$\sum_{\text{relation} \ne \text{niece}} x_{\text{relation, Y}} + \sum_{\text{Z} \ne \text{Y}} x_{\text{Z, Y}} \le 0 + M_2\sum_{\text{relation} \ne \text{brother}} x_{\text{relation, X}}$$

---

## Murder Mystery Variation

In this variation each person is a murder suspect, and the murderer is the only one who has got a weapon, a motive, and no alibi. There are many different ways to give information about this sytem, and in this iteration of the progam we will only consider a limited number of clue types. We are going to work with the condition that there is only one murderer, and that everyone has at least two out of a weapon, a motive, or no alibi. This second condition will naturally be imposed by maximising $x^T x$, and if the optimal solution does not have this satisfied then that condition cannot have been possible to satisfy. Constraints can be given on whether a person has a weapon, motive, or no alibi, and the minimum number of people who have an alibi, no weapon, or no motive. We have new rook problems, but they do not have regular rook constraints so we will call these murder grids to distinguish them. They are 3 by $n$ grids where the three columns are "weapon", "motive", and "no alibi", and the rows will sum to either 2 or 3. As we can have multiple non-zero variables in each row, we need to constrain each variable individually to be less than or equal to 1 as asking the sum to be less than equal to 3 allows the possibility of one of (3, 0, 0) being feasible.

We will impose the condition that there is one murderer by using an indicator variable for each property within a group that is equal to 1 if and only if it is the property of the murderer, and insisting that the sum of these indicator variables is at most 1. For each row in a murder grid we will have an indicator variable, and we only want it to be equal to 1 if all variables in that row are 1. For a property, X, we introduce the constraint ${x_{\text{X, weapon}} + x_{\text{X, motive}} + x_{\text{X, no alibi}} - z_{\text{X}} \le 2.5}$ and show that $z_{\text{X}}$ works as an indicator variable for X being a property of the murderer given a suitable modification to the profit function. If two of the row variables are 1 then $z_{\text{X}}$ can be 0, but if all three of them are 1 then the inequality breaks unless $z_{\text{X}}$ is non-zero. For a given group we impose the constraint that ${\sum_{\text{X} \in \text{group}} z_{\text{X}} \le 1}$, and this corresponds to the condition that there is only one murderer. It is possible however that $z_{\text{X}} = 0.5 = z_{\text{Y}}$ and multiple people are allowed to share the role of murderer. We remove this possibility by adding a $z^Tz$ term to our profit function which will force each $z_{\text{X}}$ to take on integer values, specically either 0 or 1. We note that this is consistent with the rest of the problem, as having $z_{\text{X}} = 1$ only happens when as many $x$ in that row are equal to 1, so increasing $z_{\text{X}}$ won't force the grid variable part of the profit function to decrease.

If we are told that at least $N$ people have no weapon for example, we can take the variables in the weapon column of each murder grid and insist they sum to less than or equal to $n - N$. For each cell in the murder grid we will actually need a pair variable where they are related by ${x_{\text{X}} + x'_{\text{X}} = 1}$ which is imposed by the constraint ${x_{\text{X}} + x'_{\text{X}} \le 1}$ where a dash denotes the pair variable. This is because if we are given the clue "X has a weapon" then we cannot impose the constraint $x_{\text{X}} \ge 1$ directly as the origin has to remain a feasible point. We can encode this information with a valid constraint using the pair variable however by insisting that ${x'_{\text{X}} \le 1}$. The information that property X does not have a weapon can be encoded similarly with the constraint ${x_{\text{X}} \le 1}$, and we also note that ${x_{\text{X}} + x'_{\text{X}} \le 1}$ does not add any constraints because it implies ${x_{\text{X}} \le 1}$ and ${x'_{\text{X}} \le 1}$ which we already noted where necessary constraints. This is also reminincent of how positive constraints were encoded with the original rook problems.

The only thing we need to consider now are the consistency constraints. This situation is slightly different to before as if property X has a weapon and property Y has a weapon, it does not necessarily imply that property X and property Y are properties of the same element. We instead have the weaker negative condition where if property X has a weapon and property Y does not, then properties X and Y cannot be properties of the same element. As before we consider the ${2^3 = 8}$ cases and use the same notation as in our earlier analysis of consistency.

<ol type="A">
  <li>Nationality and drink</li>
  <li>Weapon and nationality</li>
  <li>Weapon and drink</li>
</ol>

We have a similar situation to earlier, where AbC and ABc are inconsistent, but the case aBC corresponds to two different people who both have a weapon, and this is consistent. In the cases AbC and ABc, we know that as nationality and drink match, they are properties of the same person, so the properties must either both have a weapon or both not have a weapon. Our earlier consistency constraints motivate the following:

$$\text{AbC}: x_{\text{Brit, milk}} + x_{\text{weapon, Brit}} + x'_{\text{weapon, milk}} \le 2$$

$$\text{ABc}: x_{\text{Brit, milk}} + x'_{\text{weapon, Brit}} + x_{\text{weapon, milk}} \le 2$$

If the Brit does not drink milk then ${x_{\text{Brit, milk}} = 0}$ and the other two terms in both constraints can be at most 1 so the constraints are satisified as expected in all four of these cases. If the Brit does drink milk and we are in one of the two cases that are consistent, we get a contribution of 1 from the ${x_{\text{Brit, milk}}}$ term, and a contribution of 1 from only one of the other terms in each constraint, so again the constraints are satisfied. In the two inconsistent cases we see that in one of the constraint corresponding to each case, all three of the terms are equal to 1 and the contraint would break. Therefore we have found if and only if conditions for consistency of the murder properties.

---

## Well Posedness and Finding Multiple Solutions

If a problem has a solution then it will be in the feasible region. We also know that due to the rook constraints that the total of all the variables in the grid can be easily found as some value, $N$, and because we are maximising $x^Tx$ with each ${x_i \le 1}$, the profit function can only achieve $N$ if all variables are 0 or 1. If an optimal point is found with the maximal profit we know that it will be a valid solution as if any variables are not 0 or 1 then the profit would be able to be increased past the upper bound for the profit. This follows from the arguments made in the section [Choice of Profit Function](#choice-of-profit-function). A solution exists if and only if the maximum profit is $N$, and if a feasible point has maximal profit then it is a valid solution.

Finding multiple solutions can be achieved through an iterative process. An optimal point is found and some grid variables will be 0 and some will be 1. We will search for other solutions by adding a constraint to remove this point from the feasible region and attempting to optimise the problem again. We can do this by choosing a constraint that adds up all the grid variables that are equal to 1 and insisting that this sum is bounded by ${N - 1}$. As the sum of variables equal to 1 in this solution add to $N$, the point that has just been found would not be feasible with this new constraint. We also note that we do not remove any other solutions with this constraint as the only way a solution can lie beyond this constraint hyperplane is if it is identically equal to the old solution. This follows from the rook constraints.

---

## Program Structure and Implementation

Characteristic types:
- Standard: these are qualitative characteristics such as nationality, drink preference, and pet. Most characteristics in a problem will be of this type.
- Quantitative: this is something like age or height, and has more ways of interacting with than standard characteristics.
- Family: this is a special characteristic where the elements are related to each other in a family tree like structure.
- Murder: these are "No Alibi", "Weapon", and "Motive", and are used in the murder mystery variation of the problem.

Each rook problem has two characteristics associated with it. Again we split into groups based on how the characteristic types interact with each other. For example information about how two different standard characteristics is handled differently than how a pair of standard and quantitative characteristics is handled. We will only ever have one family characteristic so will not need a class for two family characteristics interacting with each other, although a family class without a pair can handle clues such as "There is only one only child", although we do not currently consider such clues. Each of "No Alibi", "Weapon", and "Motive" should be objects of a murder characteristic class, and interactions between them should be handled by a class that deals with murder characteristics at a higher level of scope. This will perform a similar role to a rook problem class that handles all the other rook problems.

Consistency constraints handle three different characteristics, and we split the ways that consistency constraints for the different triples of characteristic are handled into groups. All consistency constraints involving murder characteristics can be handled the same, and all consistency constraints not involving murder characteristics can be handled the same. We have a class for consistency constraints involving murder characteristics, and a class for consistency constraints involving non murder characteristics. An instance of the non-murder characteristics consistency class will have three rook problem objects associated with it corresponding to three different characteristics, and an instance of the murder characteristics consistency class will have 2 rook problem objects and a murder object associated with it.

Getting input on the structure of the program will be handled by a problem structure class, and this will also save the results to files, and read it again when needed. We will have a similar class for clue data. Displaying the problem output to the problem will also need it's own class. These peripheral classes and the main classes mentioned in the preceding paragraphs will be managed to by an overarching class which will be controlled by an interface script.

---

## Family Tree Construction

### Validity Constraints

We will describe people's position in the family tree as a list of directions of how to get there from the reference element. The possible directions that can be taken are "Son", "Daughter", "Mother", "Father", "Brother", "Sister", "Wife", and "Husband", so for example, mother-in-law would be "Wife, Mother" or "Husband, Mother". We use recursion to generate all possible relations, and then filter out bad relations. We are only allowing unique entities at each level, for example, two brothers are both described as male siblings, but a brother and a sister are distinguishable by their gender, so they are valid. When we generate the relations, there is only one option for "Brother", so it is impossible for someone to have relations "Brother 1" and "Brother 2", and similarly for other relations. There are some relations generated that would not be valid however, and we list them below.

- Spouse-spouse. We are assuming monogamous relationships as we need indistinguisable entities at each level. The husband of a husband, the wife of a wife, the wife of a husband or the husband of a wife of someone would be themselves in a two person relationship, so we can remove these relations. These situations are characterised by any relations that have two spousal relations next to each other.
- Sibling-sibling. "Brother, Brother" and "Sister, Sister" can either describe a situation where there are two siblings or more than two siblings. In the case of two siblings, the relations cancel out, and in the case of more than two siblings, the two siblings of the same gender would be indistinguishable. In either case it is either unnecessay or invalid so we remove them. A similar analysis shows "Brother, Sister" and "Sister, Brother" are also unnecessary or invalid.
- Parent-child and child-parent. The first relation either refers to a sibling, step-sibling or cancels out, so in either case it can be ruled out. The second relation either refers to a spouse, step-spouse, or cancels out so can also be ruled out.
- Parent-spouse, child-sibling, sibling-parents, and spouse-child. Each of these reduce down to parent, child, parents, and child respectively. In the first two the first relation is an unnecessary detour, and in the last two the second relation is an unnecessary detour.

### Structure Constraints

Further constraints can be placed on the structure of the family to reduce the number of relations, such as number of generations. At this stage the way we have generated the list of all relations mean that for any validly-shaped family tree, the relations of the other elements from any element will be in the tree. This means that any element could be the reference element. By applying further constraints on the family tree the symmetry of who can be the reference element is broken, so these constraints need to be chosen carefully by the user. For example if we only consider older generations, the reference element would have to be in the youngest generation. Not all structure constraints can be applied at this stage however. For example we cannot enforce the constraint that all children have no siblings. We need to include the possibility of the children being male or female, We list all such optional constraints currently implemented below.

- No step family. This describes the situation where "Husband" or "Wife" can only come at the end of a relation, and means the reference element will have no step relations. Only blood relations are allowed, apart from people's spouses.
- No spouses allowed. This is an even more restricted version of the above constraint. All people will be related by blood to the reference element.
- No same-sex relations. This is not actually automatically invalid by the rule that we cannot have any indistinguishible elements, as long as the only route to the spouse is as a spouse. By this we mean that you cannot have "Child, Father, Husband", as "Father" would be ambiguous. Any such cases like this are handled by the parent-spouse restriction above. This can be imposed to simplify problems however and reduce the number of relations if that is necessary.

We note that the choice of reference element can change the shape of the family. For example if the reference element is male and has two siblings of different gender, it would be impossible to change the reference element to the sister, as they would have two indistinguishable male siblings. We cobjecture that this will not be an issue however as we generate all possible relations from the reference element, and this will give the formulation enough freedom to work around any such problems.

### Names of Relations

The current description of a relation is unique, but it can be long and not human-friendly, so we would like to come up with a better label for each relation. If we try and preserve all the information then we will have a naming system just as verbose as we currently do, for example "Mother, Mother, Mother, Mother" could translate as "Maternal grandmother's maternal grandmother". "Maternal/Paternal" also become less useful as you go down branches. Piblings and spouses of n-parents can be described uniquelly, for example "Mother, Brother" translates as "Maternal uncle", but we already run into trouble when describing counsins. Niblings have gendered labels so can be specified, but the gender of the cousin would also need to be specified to uniquelly describe the nibling. To get around such awkwardness we ignore the gender of the people taken on the route to each relation when assigning a name. We do this except for the last relation when they are closely related (apart from cousin where there is no gendered word), so we still use words such as "Great-Uncle" and "Nephew". We will follow the usual naming system for position in a family tree. This is done by describing how many generations you go to get to a common ancestor, and how many you go down in the following way.

- Up 1 generation: parents
- Up $n$ generations, $n \ge 2$: $(n-2)$ great-grandparents
- Up 1 generations, down 2: nibling
- Up 2 generations, down 1: pibling
- Up 1 generations, down $n$, $n \ge 3$: $(n-3)$ great-grandnibling
- Up $n$ generations, down 1, $n \ge 3$: $(n-3)$ great-grandpibling
- Up $n$ generations, down $n$ generations: $n^{\text{th}}$ cousin
- Up $n$ generations, down $m$ generations, $n > m \ge 2$: $m^{\text{th}}$ cousin, $n-m$ times removed
- Up $n$ generations, down $m$ generations, $2 \le n < m$: $n^{\text{th}}$ cousin, $m-n$ times removed

If a relation ends with "Husband" or "Wife", then we will give that the same name as if the relation did not end with "Husband" or "Wife", but add "-in-law" on the end, and change the gender to match if it is relevant. If a relation has a spousal term in the middle then we truncate the relation after the spousal term and treat that as it's own relation. We then add the relevant ownership grammar and add the label of the rest of the relation. For example, "Mother, Sister, Husband, Brother" would be labelled as "Uncle-in-law's Brother".

This motivates the following implementation. We first split a relation into components which we will refer to as "in-law components". The relations will be split whenever a spouse is given, so each component will only contain blood relations. These components will be given a name according to the blood relation naming system described above, and then stitched together with the other in-law components. To give each component a name we only need to consider how many generations up and then down it has gone. This is well-defined due to how we described the relations, as any if a relation were to go down a generation and then back up again, this would be described by the spouse or sibling of a previously considered generation. Implicit in any sibling relation is going up and down one generation, and we note this is a non-trivial change to the number of generations. For each in-law component, we are actually going to describe the spouse, so we can change the gender of the person before to match that of their spouse, and this will handle any gender issues when describing the in-law. When stitching together the in-law components there are several cases.

- Relation does not start or end with a spouse: all the components are well-defined and non trivial. They can be joined together by placing "-in-law " between each component.
- Relation ends with but does not start with a spouse: if the relation was split on the spouses then the last component would be empty. This would give a name ending in "-in-law " followed by the blank name from the empty last component. This is correct, apart from the extra " " at the end which needs to be stripped.
- Relation starts with but does not end with a spouse, and only one spouse is mentioned: the first spouse should be removed from the name, and "-in-law" should be added to the end. An example of this would be "Mother-in-law"
- Relation starts with but does not end with a spouse, and multiple spouses are mentioned: the first spouse should be removed before the usual processing, but unlike before we add the name back to the start at the end of the process. An example of this would be "Husband, Sister, Husband, Sister" which should be "Husband's brother-in-law's sister. Another option would be "Sister-in-law's sister-in-law", but this way distinguises it from "Brother, Wife, Brother, Wife".
- Relation starts and ends with a spouse, but is not a spouse: an example of this would be "Husband, Sister, Husband". "Sister, Husband" translates as "Brother-in-law", but as this is a relation to the husband, it seems like we would need to add "-in-law" to the end of this. Instead we opt to refer to this as "Husband's brother-in-law". The first spousal relation is removed and the rest is processed in the same way as the previous case, and then the spousal name is added at the start.
- Relation is a spouse: this case is very simple, it is just the name of the spousal relation with no changes needed.

## Clue Structure

Each clue is split into a choice of subclues, so it is in the form "at least one of subclue 1,$\dots$, subclue $n$ hold". A subclue is something that gives one piece of information, and any clue that gives one piece of information will be formulated as a choice of a single subclue. We split the subclues into three main types.

- Regular clues. These relate the various characteristics together and are of the form "The relation between property X and property Y is true/false". "The Brit lives in the red house", "The Norwegian lives next to the blue house", "The person who drinks water has an uncle who keeps horses", and "The german has no alibi" are all examples of subclues. These subclues need to be further split up based on the types of characteristics they involve.
- Family clues. These clues give information about the structure of the family, but do not fit into the structure of a regular clue. For example specifying that an element is an only child, that an element is in the highest generation in the family, or specifying how many elements are at the same level of another element.
- Murdery mystery clues. These clues give information about the ways people are guilty or not guilty, but do not fit into the structure of a regular clue. Examples include giving information about how many people have an alibi, or the number of people who have exactly two of the requirements to be a murderer.

### Regular Clues

We split these into subtypes. Clues that relate two concrete properties together are the main type. An example would be "The person who lives in the second house is the person who keeps cats", and a non-example would be "The person who is neighbours with the second house is the person who keeps cats". This non-example is the second subtype, a quantitive relation. This relates two concrete properties via a quantitive characteristic. In the example of "The white house is to the left of the green house", the two concrete properties are "White" and "Green" and house order is the quantitive characteristic. The third type is family relations. This is where any two concrete properties are related via a relation. We do not currently include the case of non-concrete properties being linked via a quantitive characteristic such as "The uncle of the person who smokes blends is neighbours with the person who drinks beer", or "The neighbour of the person who smokes blends has an uncle who drinks beer".
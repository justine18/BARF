$title BARF Modell

options
limrow=1e09
;

Sets
p products
c components 
i intestinals
INT(c)
FISH(p)
BEEF(p)
LAMB(p)
CHICKEN(p);

Parameters
price(p)        price of product p
volume(p)       volume of a pack of product p
inventory(p)    inventory of product p
fat(p)          fat of product p
content_components(p,c) 
intestinal_components(p,i)
intestinal_share(i)
demand(c)
;


Scalars
weeks 'weeks to pack'
weight 'dogs weight'
perc 'percent of dogs body weight'
activity 'dogs activity level'
fatlb lower bound of fat    
fatub upper bound of fat
daylydemand
weeklydemand  
;

positive variables
X(p)    indicates selected amount of product p
;

integer variable
Y(p)
Z(p)    number of packs to buy
;

free Variable
f       objective value
;

Equations
objective   Objective Function
total       Total
totalUB     Total
components
intestinal_constraints
fishday
fat_UB
fat_LB
buy
rounding
;

objective.. f =e= sum(p, price(p) * Z(p));
total.. sum(p, X(p)) =g= 0.98 * weeklydemand * weeks;
totalUB.. sum(p, X(p)) =l= 1.02 * weeklydemand * weeks;
components(c).. sum(p, content_components(p,c) * X(p)) =g= demand(c) - 26;
intestinal_constraints(i).. sum(p, intestinal_components(p,i) * X(p)) =g= intestinal_share(i) * sum(c$INT(c), demand(c));
fishday.. sum(FISH(p), X(p)) =e= 500 * weeks;
fat_LB.. sum(p, fat(p) * X(p)) =g= fatlb * sum(p, X(p));
fat_UB.. sum(p, fat(p) * X(p)) =l= fatub * sum(p, X(p)); 
buy(p).. inventory(p) + volume(p) * Z(p) =g= X(p);
rounding(p).. X(p) =e= 50 * Y(p);

model BARF /all/;

$gdxIn 'data.gdx';
$load p, c, i
$load INT, FISH, BEEF, LAMB, CHICKEN
$load price, volume, demand, inventory
$load content_components, intestinal_components
$load intestinal_share
$load fatlb, fatub, fat
$load weeks, weeklydemand
$gdxIn

display inventory;

solve BARF minimizing f using MIP;

display X.l, Z.l;


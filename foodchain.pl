% Producers
eats(rabbit, grass).
eats(mouse, grass).
eats(deer, grass).
eats(grasshopper, grass).

% Insects and small prey
eats(frog, grasshopper).
eats(snake, mouse).
eats(snake, frog).

% Mid-level predators
eats(fox, rabbit).
eats(fox, mouse).
eats(hawk, mouse).
eats(hawk, snake).
eats(owl, mouse).
eats(owl, frog).

% Top predators
eats(wolf, deer).
eats(wolf, rabbit).
eats(bear, deer).
eats(bear, fish).
eats(eagle, hawk).
eats(eagle, fish).

% Isolated branch (aquatic, no link to land chain except via bear/eagle)
eats(fish, algae).

food_chain(X, Y) :- eats(X, Y).
food_chain(X, Y) :- eats(X, Z), food_chain(Z, Y).

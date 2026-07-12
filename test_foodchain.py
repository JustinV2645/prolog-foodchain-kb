import janus_swi as janus

# Load the same knowledge base file used in SWI-Prolog directly
janus.consult("foodchain.pl")

print("=== Basic fact queries ===")

result = list(janus.query("eats(fox, rabbit)"))
print(f"eats(fox, rabbit) -> {'true' if result else 'false'}")

result = list(janus.query("eats(fox, grass)"))
print(f"eats(fox, grass) -> {'true' if result else 'false'}")

print("\n=== Recursive rule queries ===")

result = list(janus.query("food_chain(wolf, grass)"))
print(f"food_chain(wolf, grass) -> {'true' if result else 'false'}")

result = list(janus.query("food_chain(eagle, grass)"))
print(f"food_chain(eagle, grass) -> {'true' if result else 'false'}")

result = list(janus.query("food_chain(eagle, algae)"))
print(f"food_chain(eagle, algae) -> {'true' if result else 'false'}")

result = list(janus.query("food_chain(fox, algae)"))
print(f"food_chain(fox, algae) -> {'true' if result else 'false'}")

print("\n=== Find all X such that food_chain(X, grass) ===")

results = list(janus.query("food_chain(X, grass)"))
for r in results:
    print(f"X = {r['X']}")

print(f"\nTotal solutions found: {len(results)}")

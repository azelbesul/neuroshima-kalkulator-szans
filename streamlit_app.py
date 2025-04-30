import streamlit as st
import itertools

# Poziomy trudności z modyfikatorami
difficulty_levels = {
"Fart": -15,
"Cholernie Trudny": -11,
"Bardzo Trudny": -8,
"Trudny": -5,
"Problematyczny": -2,
"Przeciętny": 0,
"Łatwy": 2,
}

def get_effective_difficulty(difficulty_name, skill_level):
levels = list(difficulty_levels.items())
idx = [i for i, (name, _) in enumerate(levels) if name == difficulty_name][0]
if skill_level >= 4:
idx = max(0, idx - 1)
return levels[idx][1]

def check_if_success(rolls, attr, skill, modifier):
ones = rolls.count(1)
twenties = rolls.count(20)
effective_mod = modifier + ones * 2 - twenties * 3
target = attr + effective_mod

auto_success = ones
auto_failure = twenties
remaining = [r for r in rolls if r != 1 and r != 20]

# Prosty przypadek: nie trzeba rozdzielać punktów umiejętności
if skill == 0:
successes = sum(1 for r in remaining if r <= target)
return (successes + auto_success - auto_failure) >= 2

# Próbujmy różnych rozdziałów punktów
for combo in itertools.product(range(skill + 1), repeat=len(remaining)):
if sum(combo) > skill:
continue
successes = auto_success
for r, cost in zip(remaining, combo):
if (r - cost) <= target:
successes += 1
if successes - auto_failure >= 2:
return True
return False

def calculate_chance(attr, skill, difficulty):
modifier = get_effective_difficulty(difficulty, skill)
rolls_all = itertools.product(range(1, 21), repeat=3)
total = 0
passed = 0

for rolls in rolls_all:
total += 1
if check_if_success(list(rolls), attr, skill, modifier):
passed += 1

return round(passed / total * 100, 2)

# Interfejs Streamlit
st.title("Neuroshima – Kalkulator Szansy na Sukces (3k20)")

attr = st.slider("Poziom współczynnika", 1, 20, 14)
skill = st.slider("Poziom umiejętności", 0, 5, 3)
difficulty = st.selectbox("Poziom trudności testu", list(difficulty_levels.keys()))

if st.button("Oblicz"):
with st.spinner("Obliczanie... może potrwać kilka sekund..."):
chance = calculate_chance(attr, skill, difficulty)
st.success(f"Szansa na sukces: **{chance}%**")

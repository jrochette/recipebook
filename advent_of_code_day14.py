from collections import Counter


initial_polymer = "KFVHFSSVNCSNHCPCNPVO"

insertion_rules = {
    "KS": "O",
    "SP": "V",
    "OH": "F",
    "VC": "P",
    "BO": "S",
    "CV": "H",
    "FO": "N",
    "KV": "V",
    "OV": "B",
    "NB": "K",
    "FS": "F",
    "KB": "N",
    "HK": "C",
    "VP": "B",
    "SV": "S",
    "FP": "P",
    "BS": "B",
    "BP": "K",
    "OS": "K",
    "PB": "C",
    "HB": "H",
    "VN": "S",
    "FB": "C",
    "OC": "N",
    "OO": "F",
    "PC": "O",
    "FK": "K",
    "OP": "V",
    "BH": "C",
    "NP": "C",
    "KF": "H",
    "SK": "F",
    "HN": "O",
    "CB": "O",
    "SN": "N",
    "VF": "S",
    "KC": "H",
    "HF": "V",
    "NC": "P",
    "BN": "F",
    "KO": "C",
    "PS": "B",
    "HO": "S",
    "CH": "O",
    "KP": "K",
    "VK": "V",
    "BB": "V",
    "BF": "P",
    "CS": "K",
    "CN": "H",
    "PK": "C",
    "SH": "O",
    "BC": "H",
    "FN": "N",
    "BK": "N",
    "PN": "B",
    "PO": "O",
    "SC": "S",
    "NO": "S",
    "KN": "O",
    "VB": "C",
    "SF": "H",
    "FH": "C",
    "FF": "B",
    "VO": "S",
    "PH": "F",
    "CK": "B",
    "FC": "P",
    "VV": "F",
    "VH": "O",
    "OF": "O",
    "HP": "K",
    "CO": "V",
    "VS": "V",
    "SB": "F",
    "SS": "K",
    "CF": "O",
    "OK": "V",
    "ON": "B",
    "NS": "H",
    "SO": "B",
    "NV": "V",
    "NH": "B",
    "NN": "K",
    "KH": "H",
    "FV": "B",
    "KK": "N",
    "OB": "F",
    "NK": "F",
    "CC": "S",
    "PP": "B",
    "PF": "H",
    "HC": "P",
    "PV": "F",
    "BV": "N",
    "NF": "N",
    "HV": "S",
    "HH": "C",
    "HS": "O",
    "CP": "O",
}


initial_pairs = {}
for i in range(len(initial_polymer) - 1):
    pair = f"{initial_polymer[i]}{initial_polymer[i+1]}"
    initial_pairs[pair] = initial_pairs.get(pair, 0) + 1


def compute_next_polymer2(polymer):
    new_polymer = {}
    for pair in polymer:
        if pair in insertion_rules:
            number_of_pair = polymer[pair]
            # Get new element
            new_element = insertion_rules[pair]

            # Add pairs with first element and new element
            new_pair_with_first_element = f"{pair[0]}{new_element}"
            new_polymer[new_pair_with_first_element] = (
                new_polymer.get(new_pair_with_first_element, 0) + number_of_pair
            )

            # Add pairs with new element and second element
            new_pair_with_second_element = f"{new_element}{pair[1]}"
            new_polymer[new_pair_with_second_element] = (
                new_polymer.get(new_pair_with_second_element, 0) + number_of_pair
            )
        else:
            new_polymer[pair] = polymer[pair]

    return new_polymer


def grow_polymer(initial_polymer, steps):
    initial_pairs = {}
    for i in range(len(initial_polymer) - 1):
        pair = f"{initial_polymer[i]}{initial_polymer[i+1]}"
        initial_pairs[pair] = initial_pairs.get(pair, 0) + 1

    polymer_map = dict(initial_pairs)
    for i in range(steps):
        polymer_map = compute_next_polymer2(polymer_map)

    element_counts = {}
    for pair in polymer_map:
        count = polymer_map[pair]
        element_counts[pair[0]] = element_counts.get(pair[0], 0) + count
        element_counts[pair[1]] = element_counts.get(pair[1], 0) + count

    # Add one to account for first and last char
    element_counts[initial_polymer[0]] = element_counts[initial_polymer[0]] + 1
    element_counts[initial_polymer[-1]] = element_counts[initial_polymer[-1]] + 1

    element_counts = sorted(list(Counter(element_counts).values()))
    print((element_counts[-1] - element_counts[0]) / 2)


grow_polymer(initial_polymer, 10)

grow_polymer(initial_polymer, 40)

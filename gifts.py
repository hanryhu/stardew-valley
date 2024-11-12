#!/usr/bin/env python

from pprint import pprint
import itertools
import logging
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)

# Dict of loved gifts from stardew 1.6 (wiki accessed 2024/11/11)
LOVED_GIFTS = {
    'haley': ['coconut', 'fruit salad', 'pink cake', 'sunflower'],
    'jas': ['ancient doll', 'fairy box', 'fairy rose', 'pink cake', 'plum pudding', 'strange doll'],
    'marnie': ['diamond', 'farmers lunch', 'pink cake', 'pumpkin pie'],
    'vincent': ['cranberry candy', 'frog egg', 'ginger ale', 'grape', 'pink cake', 'snail'],
    'abigail': ['amethyst', 'banana pudding', 'blackberry cobbler', 'chocolate cake', 'monster compendium', 'pufferfish', 'pumpkin', 'spicy eel'],
    'alex': ['complete breakfast', 'jack be nimble jack be thick', 'salmon dinner'],
    'caroline': ['fish taco', 'green tea', 'summer spangle', 'tropical curry'],
    'clint': ['amethyst', 'aquamarine', 'artichoke dip', 'emerald', 'fiddlehead risotto', 'gold bar', 'iridium bar', 'jade', 'omni geode', 'ruby', 'topaz'],
    'demetrius': ['bean hotpot', 'ice cream', 'rice pudding', 'strawberry'],
    'dwarf': ['amethyst', 'aquamarine', 'emerald', 'jade', 'lava eel', 'lemon stone', 'omni geode', 'ruby', 'topaz'],
    'elliott': ['crab cakes', 'duck feather', 'lobster', 'pomegranate', 'squid ink', 'tom kha soup'],
    'emily': ['amethyst', 'aquamarine', 'cloth', 'emerald', 'jade', 'parrot egg', 'ruby', 'survival burger', 'topaz', 'wool'],
    'evelyn': ['beet', 'chocolate cake', 'diamond', 'fairy rose', 'raisins', 'stuffing', 'tulip'],
    'george': ['fried mushroom', 'leek'],
    'gus': ['diamond', 'escargot', 'fish taco', 'orange', 'tropical curry'],
    'jodi': ['chocolate cake', 'crispy bass', 'diamond', 'eggplant parmesan', 'fried eel', 'pancakes', 'rhubarb pie', 'vegetable medley'],
    'kent': ['fiddlehead risotto', 'roasted hazelnuts'],
    'lewis': ['autumns bounty', 'glazed yams', 'green tea', 'hot pepper', 'vegetable medley'],
    'linus': ['blueberry tart', 'cactus fruit', 'coconut', 'dish o the sea', 'the alleyway buffet', 'yam'],
    'maru': ['battery pack', 'cauliflower', 'cheese cauliflower', 'diamond', 'dwarf gadget', 'gold bar', 'iridium bar', 'miners treat', 'pepper poppers', 'radioactive bar', 'rhubarb pie', 'strawberry'],
    'pam': ['beer', 'cactus fruit', 'glazed yams', 'mead', 'pale ale', 'parsnip', 'parsnip soup', 'pina colada'],
    'penny': ['diamond', 'emerald', 'melon', 'poppy', 'poppyseed muffin', 'red plate', 'roots platter', 'sandfish', 'tom kha soup'],
    'pierre': ['fried calamari', 'price catalogue'],
    'robin': ['goat cheese', 'peach', 'spaghetti', 'woodys secret'],
    'sam': ['cactus fruit', 'maple bar', 'pizza', 'tigerseye'],
    'sandy': ['crocus', 'daffodil', 'mango sticky rice', 'sweet pea'],
    'sebastian': ['frog egg', 'frozen tear', 'obsidian', 'pumpkin soup', 'sashimi', 'void egg'],
    'shane': ['beer', 'hot pepper', 'pepper poppers', 'pizza'],
    'wizard': ['book of mysteries', 'purple mushroom', 'solar essence', 'super cucumber', 'void essence'],
    'harvey': ['coffee', 'pickles', 'super meal', 'truffle oil', 'wine'],
    'krobus': ['diamond', 'iridium bar', 'monster compendium', 'monster musk', 'pumpkin', 'void egg', 'void mayonnaise', 'wild horseradish'],
    'leah': ['goat cheese', 'poppyseed muffin', 'salad', 'stir fry', 'truffle', 'vegetable medley', 'wine'],
    'leo': ['duck feather', 'mango', 'ostrich egg', 'parrot egg', 'poi'],
    'willy': ['catfish', 'diamond', 'gold bar', 'iridium bar', 'jewels of the sea', 'mead', 'octopus', 'pumpkin', 'sea cucumber', 'sturgeon', 'the art o crabbing'],
}



def find_gifts(all_gifts=LOVED_GIFTS):
    """
    This method finds a set cover (https://en.wikipedia.org/wiki/Set_cover_problem):

    Near-optimal solutions are available (https://github.com/guangtunbenzhu/SetCoverPy).

    This method uses a brute-force approach as there are 143 subsets.

    Used code from: https://stackoverflow.com/a/21975926
    """
    all_people = set(all_gifts.keys())
    reverse_all_gifts = {}
    for person, loved_gifts in all_gifts.items():
        for loved_gift in set(loved_gifts):
            reverse_all_gifts[loved_gift] = {person, *reverse_all_gifts.get(loved_gift, set())}

    ######################################################################
    # Prune singletons                                                   #
    ######################################################################
    seen_people = set()
    for gift, people in list(reverse_all_gifts.items()):
        if len(people) == 1:
            # Prune singleton list.
            print(f'Pruning {gift} as only {people} loves it.')
            del reverse_all_gifts[gift]
        else:
            seen_people.update(people)
    singletons = {}
    people_needing_singletons = set()
    for person in all_people:
        if person not in seen_people:
            people_needing_singletons.add(person)
            # gift = all_gifts[person][0]
            gift = f'<{person} gift>'
            print(f'Found that {person} only had singleton gifts.  Using {gift}.')
            singletons[gift] = {person}

    gift_people = all_people - people_needing_singletons

    # O(people * people * gifts) time to preprocess, very cheap
    # compared to exponential.
    for gift, people in list(reverse_all_gifts.items()):
        for other_gift, other_people in list(reverse_all_gifts.items()):
            if gift != other_gift and people <= other_people:
                # gift is dominated by other_gift
                print(f'Pruned {gift} as it is dominated by {other_gift}')
                # Even if we prune other_gift later, then it itself
                # was dominated by another gift, so it's ok to prune
                # gift
                del reverse_all_gifts[gift]
                # Already pruned this gift, consider pruning next gift.
                break

    # Doubleton pruning is wrong, the general form of singleton
    # pruning is dominated set pruning.
    
    ######################################################################
    # Prune doubletons                                                   #
    ######################################################################
    # doubleton_seen_people = set()
    # doubletons = {}
    # for gift, people in list(reverse_all_gifts.items()):
    #     if len(people) == 2:
    #         # Prune doubleton list.
    #         print(f'Pruning {gift} as only {people} love it.')
    #         doubletons[gift] = people
    #         del reverse_all_gifts[gift]
    #     else:
    #         doubleton_seen_people.update(people)
    # people_needing_doubletons = set()
    # for person in gift_people:
    #     if person not in doubleton_seen_people:
    #         people_needing_doubletons.add(person)
    # print(f'Found that {people_needing_doubletons} only had doubleton gifts.  Using mini cover with pool of {len(doubletons)} gifts.')
    # pprint(doubletons)
    # doubletons_found = []
    # for n in range(2, len(doubletons)):
    #     print(f"Trying combinations of {n} gifts out of {len(doubletons)}")
    #     for gift_combo in itertools.combinations(doubletons.keys(), n):
    #         u = set().union(*[doubletons[gift] for gift in gift_combo])
    #         if people_needing_doubletons <= u:
    #             doubletons_found.append(gift_combo)
    #     if doubletons_found:
    #         break
    # print(f'Mini cover options: {doubletons_found}')

    # Add back doubletons
    # found_with_doubletons = []
    # for combo in found:
    #     found_with_doubletons.extend(
    #         [combo + doubletons_combo for doubletons_combo in doubletons_found]
    #     )

    # gift_people = gift_people - people_needing_doubletons

    found = []
    # Tuple (n, k, sets) where n is the number of people requiring
    # singleton gifts, k is the number of non-singleton gifts, and
    # sets is a list of the near-cover sets containing singletons for
    # those people.
    max_near_cover = (len(gift_people), 0, [tuple(f'<{person} gift>' for person in gift_people)])
    for n in range(2, len(reverse_all_gifts)):
        print(f"Trying combinations of {n} gifts out of {len(reverse_all_gifts)}")
        for gift_combo in itertools.combinations(reverse_all_gifts.keys(), n):
            u = set().union(*[reverse_all_gifts[gift] for gift in gift_combo])
            if gift_people <= u:
                found.append(gift_combo)
            elif len(gift_people - u) + n < max_near_cover[0] + max_near_cover[1]:
                max_near_cover = (len(gift_people - u), n, [gift_combo + tuple(f'<{person} gift>' for person in gift_people - u)])
            elif len(gift_people - u) + n == max_near_cover[0] + max_near_cover[1] and n <= max_near_cover[1]:
                max_near_cover[2].append(gift_combo + tuple(f'<{person} gift>' for person in gift_people - u))
        if found:
            break
        else:
            if max_near_cover[1] < n:
                print(f"No more efficient gift combos found at {n} gifts.")
            else:
                print(f"For combinations of {max_near_cover[1]} gifts, the most efficient combos covered all but {max_near_cover[0]} people: {max_near_cover[2]}")

    # Add back singletons
    return [combo + tuple(singletons.keys()) for combo in found]

# Full output of the above function with default inputs:
FULL_OUTPUT = '''
>>> find_gifts()
Pruning sunflower as only {'haley'} loves it.
Pruning fruit salad as only {'haley'} loves it.
Pruning plum pudding as only {'jas'} loves it.
Pruning strange doll as only {'jas'} loves it.
Pruning fairy box as only {'jas'} loves it.
Pruning ancient doll as only {'jas'} loves it.
Pruning pumpkin pie as only {'marnie'} loves it.
Pruning farmers lunch as only {'marnie'} loves it.
Pruning snail as only {'vincent'} loves it.
Pruning ginger ale as only {'vincent'} loves it.
Pruning cranberry candy as only {'vincent'} loves it.
Pruning grape as only {'vincent'} loves it.
Pruning blackberry cobbler as only {'abigail'} loves it.
Pruning banana pudding as only {'abigail'} loves it.
Pruning spicy eel as only {'abigail'} loves it.
Pruning pufferfish as only {'abigail'} loves it.
Pruning complete breakfast as only {'alex'} loves it.
Pruning jack be nimble jack be thick as only {'alex'} loves it.
Pruning salmon dinner as only {'alex'} loves it.
Pruning summer spangle as only {'caroline'} loves it.
Pruning artichoke dip as only {'clint'} loves it.
Pruning rice pudding as only {'demetrius'} loves it.
Pruning ice cream as only {'demetrius'} loves it.
Pruning bean hotpot as only {'demetrius'} loves it.
Pruning lava eel as only {'dwarf'} loves it.
Pruning lemon stone as only {'dwarf'} loves it.
Pruning crab cakes as only {'elliott'} loves it.
Pruning lobster as only {'elliott'} loves it.
Pruning pomegranate as only {'elliott'} loves it.
Pruning squid ink as only {'elliott'} loves it.
Pruning survival burger as only {'emily'} loves it.
Pruning wool as only {'emily'} loves it.
Pruning cloth as only {'emily'} loves it.
Pruning beet as only {'evelyn'} loves it.
Pruning stuffing as only {'evelyn'} loves it.
Pruning tulip as only {'evelyn'} loves it.
Pruning raisins as only {'evelyn'} loves it.
Pruning fried mushroom as only {'george'} loves it.
Pruning leek as only {'george'} loves it.
Pruning orange as only {'gus'} loves it.
Pruning escargot as only {'gus'} loves it.
Pruning pancakes as only {'jodi'} loves it.
Pruning fried eel as only {'jodi'} loves it.
Pruning crispy bass as only {'jodi'} loves it.
Pruning eggplant parmesan as only {'jodi'} loves it.
Pruning roasted hazelnuts as only {'kent'} loves it.
Pruning autumns bounty as only {'lewis'} loves it.
Pruning dish o the sea as only {'linus'} loves it.
Pruning blueberry tart as only {'linus'} loves it.
Pruning the alleyway buffet as only {'linus'} loves it.
Pruning yam as only {'linus'} loves it.
Pruning miners treat as only {'maru'} loves it.
Pruning dwarf gadget as only {'maru'} loves it.
Pruning radioactive bar as only {'maru'} loves it.
Pruning battery pack as only {'maru'} loves it.
Pruning cauliflower as only {'maru'} loves it.
Pruning cheese cauliflower as only {'maru'} loves it.
Pruning parsnip as only {'pam'} loves it.
Pruning pale ale as only {'pam'} loves it.
Pruning parsnip soup as only {'pam'} loves it.
Pruning pina colada as only {'pam'} loves it.
Pruning red plate as only {'penny'} loves it.
Pruning roots platter as only {'penny'} loves it.
Pruning melon as only {'penny'} loves it.
Pruning sandfish as only {'penny'} loves it.
Pruning poppy as only {'penny'} loves it.
Pruning price catalogue as only {'pierre'} loves it.
Pruning fried calamari as only {'pierre'} loves it.
Pruning peach as only {'robin'} loves it.
Pruning spaghetti as only {'robin'} loves it.
Pruning woodys secret as only {'robin'} loves it.
Pruning tigerseye as only {'sam'} loves it.
Pruning maple bar as only {'sam'} loves it.
Pruning mango sticky rice as only {'sandy'} loves it.
Pruning sweet pea as only {'sandy'} loves it.
Pruning crocus as only {'sandy'} loves it.
Pruning daffodil as only {'sandy'} loves it.
Pruning pumpkin soup as only {'sebastian'} loves it.
Pruning frozen tear as only {'sebastian'} loves it.
Pruning obsidian as only {'sebastian'} loves it.
Pruning sashimi as only {'sebastian'} loves it.
Pruning solar essence as only {'wizard'} loves it.
Pruning book of mysteries as only {'wizard'} loves it.
Pruning void essence as only {'wizard'} loves it.
Pruning super cucumber as only {'wizard'} loves it.
Pruning purple mushroom as only {'wizard'} loves it.
Pruning super meal as only {'harvey'} loves it.
Pruning truffle oil as only {'harvey'} loves it.
Pruning pickles as only {'harvey'} loves it.
Pruning coffee as only {'harvey'} loves it.
Pruning wild horseradish as only {'krobus'} loves it.
Pruning monster musk as only {'krobus'} loves it.
Pruning void mayonnaise as only {'krobus'} loves it.
Pruning salad as only {'leah'} loves it.
Pruning truffle as only {'leah'} loves it.
Pruning stir fry as only {'leah'} loves it.
Pruning poi as only {'leo'} loves it.
Pruning ostrich egg as only {'leo'} loves it.
Pruning mango as only {'leo'} loves it.
Pruning sea cucumber as only {'willy'} loves it.
Pruning octopus as only {'willy'} loves it.
Pruning the art o crabbing as only {'willy'} loves it.
Pruning sturgeon as only {'willy'} loves it.
Pruning catfish as only {'willy'} loves it.
Pruning jewels of the sea as only {'willy'} loves it.
Found that george only had singleton gifts.  Using <george gift>.
Found that pierre only had singleton gifts.  Using <pierre gift>.
Found that sandy only had singleton gifts.  Using <sandy gift>.
Found that alex only had singleton gifts.  Using <alex gift>.
Found that wizard only had singleton gifts.  Using <wizard gift>.
Pruned monster compendium as it is dominated by pumpkin
Pruned tropical curry as it is dominated by fish taco
Pruned gold bar as it is dominated by iridium bar
Pruned omni geode as it is dominated by amethyst
Pruned jade as it is dominated by amethyst
Pruned topaz as it is dominated by amethyst
Pruned aquamarine as it is dominated by amethyst
Pruned ruby as it is dominated by amethyst
Pruned rhubarb pie as it is dominated by diamond
Trying combinations of 2 gifts out of 29
For combinations of 2 gifts, the most efficient combos covered all but 17 people: [('diamond', 'amethyst', '<sebastian gift>', '<linus gift>', '<lewis gift>', '<elliott gift>', '<haley gift>', '<sam gift>', '<harvey gift>', '<caroline gift>', '<leah gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<jas gift>', '<robin gift>', '<pam gift>', '<vincent gift>')]
Trying combinations of 3 gifts out of 29
For combinations of 3 gifts, the most efficient combos covered all but 14 people: [('pink cake', 'diamond', 'amethyst', '<sebastian gift>', '<linus gift>', '<lewis gift>', '<elliott gift>', '<sam gift>', '<harvey gift>', '<caroline gift>', '<leah gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>', '<pam gift>'), ('diamond', 'amethyst', 'cactus fruit', '<sebastian gift>', '<lewis gift>', '<elliott gift>', '<haley gift>', '<harvey gift>', '<caroline gift>', '<leah gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<jas gift>', '<robin gift>', '<vincent gift>')]
Trying combinations of 4 gifts out of 29
For combinations of 4 gifts, the most efficient combos covered all but 11 people: [('pink cake', 'diamond', 'amethyst', 'cactus fruit', '<sebastian gift>', '<lewis gift>', '<elliott gift>', '<leah gift>', '<harvey gift>', '<caroline gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>')]
Trying combinations of 5 gifts out of 29
For combinations of 5 gifts, the most efficient combos covered all but 9 people: [('pink cake', 'diamond', 'amethyst', 'green tea', 'cactus fruit', '<sebastian gift>', '<elliott gift>', '<leah gift>', '<harvey gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'cactus fruit', '<sebastian gift>', '<lewis gift>', '<leah gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'vegetable medley', 'cactus fruit', '<sebastian gift>', '<elliott gift>', '<leo gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'hot pepper', 'cactus fruit', '<sebastian gift>', '<elliott gift>', '<leah gift>', '<harvey gift>', '<caroline gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<lewis gift>', '<elliott gift>', '<leo gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>'), ('pink cake', 'diamond', 'amethyst', 'cactus fruit', 'wine', '<sebastian gift>', '<lewis gift>', '<elliott gift>', '<leo gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>')]
Trying combinations of 6 gifts out of 29
For combinations of 6 gifts, the most efficient combos covered all but 7 people: [('pink cake', 'diamond', 'amethyst', 'green tea', 'duck feather', 'cactus fruit', '<sebastian gift>', '<leah gift>', '<harvey gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<elliott gift>', '<leo gift>', '<harvey gift>', '<demetrius gift>', '<kent gift>', '<shane gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'cactus fruit', 'wine', '<sebastian gift>', '<elliott gift>', '<leo gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'vegetable medley', 'cactus fruit', '<sebastian gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'hot pepper', 'cactus fruit', '<sebastian gift>', '<leah gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<lewis gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'cactus fruit', 'wine', '<sebastian gift>', '<lewis gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'hot pepper', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<elliott gift>', '<leo gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>'), ('pink cake', 'diamond', 'amethyst', 'hot pepper', 'cactus fruit', 'wine', '<sebastian gift>', '<elliott gift>', '<leo gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<robin gift>')]
Trying combinations of 7 gifts out of 29
For combinations of 7 gifts, the most efficient combos covered all but 5 people: [('pink cake', 'diamond', 'amethyst', 'green tea', 'duck feather', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<harvey gift>', '<demetrius gift>', '<kent gift>', '<shane gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'duck feather', 'cactus fruit', 'wine', '<sebastian gift>', '<demetrius gift>', '<kent gift>', '<shane gift>', '<robin gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'hot pepper', 'cactus fruit', 'goat cheese', '<sebastian gift>', '<harvey gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>'), ('pink cake', 'diamond', 'amethyst', 'duck feather', 'hot pepper', 'cactus fruit', 'wine', '<sebastian gift>', '<caroline gift>', '<demetrius gift>', '<kent gift>', '<robin gift>')]
Trying combinations of 8 gifts out of 29
No more efficient gift combos found at 8 gifts.
Trying combinations of 9 gifts out of 29
No more efficient gift combos found at 9 gifts.
Trying combinations of 10 gifts out of 29
No more efficient gift combos found at 10 gifts.
Trying combinations of 11 gifts out of 29
No more efficient gift combos found at 11 gifts.
Trying combinations of 12 gifts out of 29
[('pink cake', 'diamond', 'frog egg', 'amethyst', 'fish taco', 'fiddlehead risotto', 'strawberry', 'duck feather', 'hot pepper', 'cactus fruit', 'goat cheese', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'frog egg', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'hot pepper', 'cactus fruit', 'goat cheese', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'frog egg', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'pepper poppers', 'goat cheese', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'frog egg', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'beer', 'goat cheese', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'frog egg', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'goat cheese', 'pizza', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'amethyst', 'fish taco', 'fiddlehead risotto', 'strawberry', 'duck feather', 'hot pepper', 'cactus fruit', 'goat cheese', 'void egg', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'hot pepper', 'cactus fruit', 'goat cheese', 'void egg', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'pepper poppers', 'goat cheese', 'void egg', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'beer', 'goat cheese', 'void egg', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>'), ('pink cake', 'diamond', 'amethyst', 'green tea', 'fiddlehead risotto', 'strawberry', 'duck feather', 'cactus fruit', 'goat cheese', 'pizza', 'void egg', 'wine', '<george gift>', '<pierre gift>', '<sandy gift>', '<alex gift>', '<wizard gift>')]
'''

from policy import CribbagePolicy, CompositePolicy, GreedyThrower, GreedyPegger
import random
from abc import ABC, abstractmethod

import scoring

class MyPolicy(CribbagePolicy):
    def __init__(self, game):
        self._policy = CompositePolicy(game, MyThrower(game), MyPegger(game))

        
    def keep(self, hand, scores, am_dealer):
        return self._policy.keep(hand, scores, am_dealer)


    def peg(self, cards, history, scores, am_dealer):
        return self._policy.peg(cards, history, scores, am_dealer)


class ThrowPolicy(ABC):
    """ An abstract base class for cribbage keep/throw policies. """
    def __init__(self, game):
        """ Creates a policy to play the given game.

            game -- a cribbage Game
        """
        self._game = game

        
    @abstractmethod
    def keep(self, hand, scores, am_dealer):
        """ Returns a pair (keep, throw) determining which cards from the given
            hand to keep under this policy.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        pass


class PegPolicy(ABC):
    """ An abstract base class for cribbage pegging policies. """
    
    def __init__(self, game):
        """ Creates a policy to play the given game.

            game -- a cribbage Game
        """
        self._game = game

        
    @abstractmethod
    def peg(self, cards, history, scores, am_dealer):
        """ Returns the card to play from the given list.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        pass


class MyThrower(ThrowPolicy):
    """ A greedy policy for keep/throw in cribbage.  The greedy decision is
        based only on the score obtained by the cards kept and thrown, without
        consideration for how they might interact with the turned card or
        cards thrown by the opponent.
    """
    
    def __init__(self, game):
        """ Creates a greedy keep/throw policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)

    def my_throw(self, game, deal, crib):
        """ Returns a my choice of which cards to throw.  The greedy choice
        is determined by the score of the four cards kept and the two cards
        thrown in isolation, without considering what the turned card
        might be or what the opponent might throw to the crib.  If multiple
        choices result in the same net score, then one is chosen randomly.

        game -- a Cribbage game
        deal -- a list of the cards dealt
        crib -- 1 for owning the crib, -1 for opponent owning the crib
        """
        def score_split(indices):
            keep = []
            throw = []
            for i in range(len(deal)):
                if i in indices:
                    throw.append(deal[i])
                else:
                    keep.append(deal[i])

            deck = game.deck()
            deck.remove(keep)
            deck.remove(throw)
            
            calculate_score = 0

            for card in deck._cards:
                calculate_score += scoring.score(game, keep, card, False)[0] + crib * scoring.score(game, throw, card, True)[0]
            
            calculate_score = calculate_score / 46

            result_score = calculate_score

            throw_ranks = [throw[0]._rank, throw[1]._rank]

            for card in keep:
                if card._rank == 11:
                    result_score += 0.05
                if card._rank == 1 or card._rank == 2 or card._rank == 3 or card._rank == 4:
                    result_score += 0.3
                if (card._rank == 10 or card._rank == 11 or card._rank == 12 or card._rank == 13):
                    result_score -= 0.2
            
            if throw[0]._rank + throw[1]._rank == 5 and crib == 1:
                result_score -= 0.2

            return keep, throw, result_score

        throw_indices = game.throw_indices()
        
        # to randomize the order in which throws are considered to have the effect
        # of breaking ties randomly
        random.shuffle(throw_indices)

        # pick the (keep, throw, score) triple with the highest score
        return max(map(lambda i: score_split(i), throw_indices), key=lambda t: t[2])


    def keep(self, hand, scores, am_dealer):
        """ Selects the cards to keep to maximize the net score for those cards
            and the cards in the crib.  Points in the crib count toward the
            total if this policy is the dealer and against the total otherwise.

            hand -- a list of cards
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        keep, throw, net_score = self.my_throw(self._game, hand, 1 if am_dealer else -1)
        return keep, throw


class MyPegger(PegPolicy):
    """ A cribbage pegging policy that plays the card that maximizes the
        points earned on the current play.
    """

    def __init__(self, game):
        """ Creates a greedy pegging policy for the given game.

            game -- a cribbage Game
        """
        super().__init__(game)


    def peg(self, cards, history, scores, am_dealer):
        """ Returns the card that maximizes the points earned on the next
            play.  Ties are broken uniformly randomly.

            cards -- a list of cards
            history -- the pegging history up to the point to decide what to play
            scores -- the current scores, with this policy's score first
            am_dealer -- a boolean flag indicating whether the crib
                         belongs to this policy
        """
        # shuffle cards to effectively break ties randomly
        random.shuffle(cards)

        best_card = None
        best_score = None

        hand_ranks = []
        for card in cards:
            hand_ranks.append(card._rank)
   
        for card in cards:
            score = history.score(self._game, card, 0 if am_dealer else 1)
            if score is not None:
                if history.is_start_round():

                    if card._rank == 5:
                        score -= 0.5

                    if card._rank in [1, 2, 3, 10, 11, 12, 13] and 5 not in hand_ranks:
                        score -= 0.3
                    # elif card._rank in [10, 11, 12, 13] and 5 in hand_ranks:
                    #     score += 0.4
                    
                    if card._rank == 7 and (6 in hand_ranks or 9 in hand_ranks):
                        score += 0.5
                    elif card._rank == 7 and 8 in hand_ranks:
                        score += 0.4

                    if card._rank == 8 and (6 in hand_ranks or 9 in hand_ranks):
                        score += 0.5
                    elif card._rank == 8 and 7 in hand_ranks:
                        score += 0.4

                    # if (card._rank == 6 and 9 in hand_ranks) or (card._rank == 9 and 6 in hand_ranks):
                    #     score += 0.4

                new_total = history.play(self._game, card, 0 if am_dealer else 1)[0]._total
                if new_total > 4 and new_total < 15:
                    score -= 0.3

                if new_total == 21:
                    score -= 0.3

                if new_total > 28 and new_total < 31:
                    score += 0.3

                if new_total == 5:
                    score -= 0.3
                
                if new_total == 15:
                    score += 0.2
                
                # if new_total == 31:
                #     score += 0.2

            if score is not None and (best_score is None or score > best_score):
                best_score = score
                best_card = card
        return best_card

                                    

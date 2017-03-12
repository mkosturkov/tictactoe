
def get_best_moves_for_player(player, board):
    player_scores = sorted(get_scores_for_player(player, board), cmp=compare_scores, reverse=True)
    other_player_scores = sorted(get_scores_for_other_player(player, board), cmp=compare_scores, reverse=True)
    comparison_result = compare_scores(player_scores[0], other_player_scores[0])
    chosen_scores = player_scores if comparison_result > 0 else other_player_scores
    return get_top_scores(chosen_scores)
    
def get_scores_for_player(player, board):
    return get_scores(lambda p: p == player, board)

def get_scores_for_other_player(player, board):
    return get_scores(lambda p: p != player, board)

def get_scores(is_player_callback, board):
    positions = get_unmarked_positions(board)
    positions_with_lines = bind_positions_to_lines(positions, board)
    return [get_single_score(is_player_callback, pl) for pl in positions_with_lines]

def get_single_score(is_player_callback, position_with_lines):
    score = Score()
    score.positions_owned = get_most_positions_owned_in_lines_count(is_player_callback, position_with_lines['lines'])
    score.number_of_combinations = get_number_of_possible_combinations(is_player_callback, position_with_lines['lines'])
    score.position = position_with_lines['position']
    return score
    
def get_most_positions_owned_in_lines_count(is_player_callback, lines):
    most_positions = 0
    for line in lines:
        current_line = 0
        for position in line.positions:
            if position.is_marked() and is_player_callback(position.get_marked_player()):
                current_line += 1
        if current_line > most_positions:
            most_positions = current_line
    return most_positions

def get_number_of_possible_combinations(is_player_callback, lines):
    possible_combinations = len(lines)
    for line in lines:
        for position in line.positions:
            if position.is_marked() and not is_player_callback(position.get_marked_player()):
                possible_combinations -= 1
                break
    return possible_combinations
    
def get_unmarked_positions(board):
    return [position for row in board.positions for position in row if not position.is_marked()]

def bind_positions_to_lines(positions, board):
    lines = board.get_lines()
    bound = []
    for position in positions:
        bound.append({'position': position, 'lines': filter(lambda line: position in line.positions, lines)})
    return bound

def compare_scores(score1, score2):
    positions_check = score1.positions_owned - score2.positions_owned
    if positions_check != 0:
        return positions_check
    return score1.number_of_combinations - score2.number_of_combinations

def get_top_scores(scores):
    top_scores = [scores[0]]
    for i in range(1, len(scores)):
        if compare_scores(scores[0], scores[i]) == 0:
            top_scores.append(scores[i])
    return top_scores


class Score:
    
    def __init__(self, positions_owned=None, number_of_combinations=None, position=None):
        self.positions_owned = positions_owned
        self.number_of_combinations = number_of_combinations
        self.position = position
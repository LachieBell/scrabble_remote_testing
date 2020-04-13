from random import randint, seed, choice

# seed('Hello Matt Parker')

PLAYER_1 = "Player 1"
PLAYER_2 = "Player 2"

two_shuffle = {0: 9, 1: 7, 2: 5, 3: 3, 4: 1, 5: 0, 6: 2, 7: 4, 8: 6, 9: 8}
three_shuffle = {0: 8, 1: 5, 2: 2, 3: 0, 4: 1, 5: 3, 6: 4, 7: 6, 8: 7, 9: 9}


def int_to_tuple(n):

    return n // 10, n % 10


def tuple_to_int(turn):

    return 10 * turn[0] + turn[1]


def get_mapping(tile, private_key, public_key):

    tile = list(tile)
    r_1 = private_key[tile[1]]

    tile[0] += r_1
    tile[0] %= 10

    r_2 = public_key[tile[0]]

    tile[1] += r_2
    tile[1] %= 10

    tile[0] = two_shuffle[tile[0]]
    tile[0] = three_shuffle[tile[0]]

    tile[1] = two_shuffle[tile[1]]
    tile[1] = three_shuffle[tile[1]]

    return tuple(tile)


def main():
    
    private_key = [randint(0, 9) for _ in range(10)]  # x
    public_key = [randint(0, 9) for _ in range(10)]  # y

    mapped_tile_set = set()
    tiles_left = [int_to_tuple(i) for i in range(100)]

    player_1_pool = [int_to_tuple(i) for i in range(0, 100, 2)]
    player_2_pool = [t for t in tiles_left if t not in player_1_pool]

    whos_turn = PLAYER_1
    print(f"Everybody knows the public key: {public_key}")

    while len(tiles_left) > 0:

        # Basically choosing a "tile" from the grid.
        # Player 1 chooses a tile.
        if whos_turn == PLAYER_1:
            if player_1_pool:
                tile = choice(player_1_pool)
                player_1_pool.remove(tile)
            else:
                tile = choice(tiles_left)
                player_2_pool.remove(tile)
            if tile[1] % 2:
                print(
                    f"{PLAYER_1} had to ask for {PLAYER_2}'s key for index: {tile[1]}"
                )

        # Player 2 chooses a tile.
        else:
            if player_2_pool:
                tile = choice(player_2_pool)
                player_2_pool.remove(tile)
            else:
                tile = choice(tiles_left)
                player_1_pool.remove(tile)

            if not tile[1] % 2:
                print(
                    f"{PLAYER_2} had to ask for {PLAYER_1}'s key for index: {tile[1]}"
                )

        print(f"{whos_turn} chose tile {tuple_to_int(tile)} as a starting seed")

        tiles_left.remove(tile)

        mapped_tile = get_mapping(tile, private_key, public_key)
        mapped_tile = tuple_to_int(mapped_tile)
        mapped_tile_set.add(mapped_tile)

        print(f'{whos_turn} should pickup tile: {mapped_tile}')

        # 50% of the time, the next person to grab a tile is the other person.
        if randint(0, 100) >= 50:
            if whos_turn == PLAYER_1:
                whos_turn = PLAYER_2
            else:
                whos_turn = PLAYER_1

    # Asserting that we did correctly map all 100 tiles to 100 unique tiles.
    assert len(mapped_tile_set) == 100


if __name__ == "__main__":
    main()

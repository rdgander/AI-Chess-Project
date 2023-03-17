import random

import numpy as np
import chess
import Player
import math

class MoveType():
    regular = 0
    check = 1
    capture = 2
    promo = 4

class MoveHeuristic():
    def __init__(self, piece_type, from_sq=0, to_sq=0, move_type=None, promo_piece=None, position=None, see_score=None):
        self.piece_type = piece_type
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.move_type = move_type or 0
        self.promo_piece = promo_piece
        self.position = position
        self.see_score = see_score

    def __str__(self):
        if self.piece_type is None or self.piece_type == PieceType.NULL:
            return "NULL"
        return HUMAN_PIECE[self.piece_type] \
               + HUMAN_BOARD_INV[self.from_sq] \
               + "-" + HUMAN_BOARD_INV[self.to_sq] \
               + ("=" + HUMAN_PIECE[self.promo_piece] if self.move_type & MoveType.promo else "") \
               + ("+" if self.move_type == MoveType.check else "")

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.piece_type == other.piece_type \
                   and self.from_sq == other.from_sq \
                   and self.to_sq == other.to_sq \
                   and self.promo_piece == other.promo_piece
            # move_type depends on the position and we may lazily assign movetype.check
        else:
            return False

    @property
    def to_uci(self):
        result = ""
        if self.piece_type == PieceType.NULL:
            return "0000"
        from_str = HUMAN_BOARD_INV[self.from_sq]
        to_str = HUMAN_BOARD_INV[self.to_sq]
        result += from_str + to_str
        if self.move_type & MoveType.promo:
            promo_str = HUMAN_PIECE[self.promo_piece]
            result += promo_str.lower()
        return result

    def compact(self):
        # bits 0-5 from_sq
        # bits 6-11 to_sq
        # bits 12-15 piece_type
        # bits 16-19 promo_piece
        # bits 20-22 move_type
        if self.piece_type == PieceType.NULL:
            return 0
        from_sq = bit_position(self.from_sq)
        to_sq = bit_position(self.to_sq) << 6
        piece_type = self.piece_type << 12
        promo_piece = (self.promo_piece or 0) << 16
        move_type = (self.move_type or 0) << 20
        return from_sq | to_sq | piece_type | promo_piece | move_type

    def is_null_move(self):
        return self.piece_type == PieceType.NULL

    @classmethod
    def move_uncompacted(cls, compacted):
        from_sq = 1 << (compacted & 0x3f)
        to_sq = 1 << ((compacted >> 6) & 0x3f)
        piece_type = (compacted >> 12) & 0xf
        promo_piece = (compacted >> 16) & 0xf
        move_type = (compacted >> 20) & 0xf
        return cls(piece_type, from_sq, to_sq, move_type or 0, promo_piece or None)

    @classmethod
    def map_str_moves(cls, moves_list):
        return ' '.join(map(str, moves_list))
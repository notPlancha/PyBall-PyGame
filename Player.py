from dataclasses import dataclass

from pygame.rect import Rect


@dataclass
class PlayerKey:
    key: int
    isKeyPressed: bool = False

    def __eq__(self, other: int):
        return self.key == other

    def copy(self):
        return PlayerKey(self.key, self.isKeyPressed)


@dataclass
class Movement:
    posKey: PlayerKey
    negKey: PlayerKey
    acelaration: int = 2
    speed: int = 0
    Friction: int = 1

    def copy(self):
        return Movement(self.posKey.copy(), self.negKey.copy(), self.acelaration, self.currVelocity, self.Friction)


@dataclass
class Player:
    horizMovement: Movement
    vertiMovement: Movement
    color: tuple[int, int, int, [int]]
    pos: list[int, int]
    radius: float
    thickness: int = 0
    isVisible: bool = True

    def copy(self):
        return Player(self.horizMovement.copy(), self.vertiMovement.copy(), self.color, self.pos.copy(), self.radius,
                      self.thickness, self.isVisible)

class PlayerList:
    def __init__(self, *args: Player):
        self.Players: list[Player] = []
        #                                                    False : neg, True : posit
        self.keysToPlayerKey: list[tuple[PlayerKey, Movement, bool]] = []
        self.addPlayers(*args)

    def addPlayers(self, *args: Player):
        for P in args:
            self.Players.append(P)
            self.keysToPlayerKey.append((P.horizMovement.posKey, P.horizMovement, True))
            self.keysToPlayerKey.append((P.horizMovement.negKey, P.horizMovement, False))
            self.keysToPlayerKey.append((P.vertiMovement.posKey, P.vertiMovement, True))
            self.keysToPlayerKey.append((P.vertiMovement.negKey, P.vertiMovement, False))

    def fromKeyToMovements(self, key: int) -> list[tuple[PlayerKey, Movement, bool]]:
        return [i for i in self.keysToPlayerKey if i[0] == key]

    def handleKeyDown(self, key):
        key: list[tuple[PlayerKey, Movement, bool]] = self.fromKeyToMovements(key)
        for i in key:
            i[0].isKeyPressed = True

    def handleKeyUp(self, key):
        key: list[tuple[PlayerKey, Movement, bool]] = self.fromKeyToMovements(key)
        for i in key:
            i[0].isKeyPressed = False

    def __iter__(self):
        for i in self.Players:
            yield i

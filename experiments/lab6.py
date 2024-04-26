class Quantity[Mul: tuple, Div: tuple]: ...


type Quant[T] = Quantity[tuple[T], tuple[()]]
type Mul[*Ts, T] = Quantity[tuple[*Ts, T], tuple[()]]


class DISTANCE: ...


Distance = Quantity[tuple[DISTANCE], tuple[()]]

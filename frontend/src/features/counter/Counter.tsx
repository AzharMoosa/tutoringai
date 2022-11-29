import React from "react";
import { useAppSelector, useAppDispatch } from "../../hooks/redux/hooks";
import { increment } from "./counterSlice";

const Counter = () => {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();
  return (
    <div>
      <h1>Counter {count}</h1>
      <button onClick={() => dispatch(increment())}>s</button>
    </div>
  );
};

export default Counter;

import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import CartPage from "../app/cart/page";

describe("Cart Page", () => {
  it("renders the cart page", () => {
    render(<CartPage />);
    expect(screen.getByText("Desk Vase")).toBeInTheDocument();
    expect(screen.getByText("Subtotal")).toBeInTheDocument();
    expect(screen.getByText("Shipping")).toBeInTheDocument();
    expect(screen.getByText("Cancel cart")).toBeInTheDocument();
  });
});

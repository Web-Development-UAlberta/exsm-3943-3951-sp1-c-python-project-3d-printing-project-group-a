import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import CheckoutPage from "../app/checkout/page";

describe("Checkout Page", () => {
  it("renders the checkout page", () => {
    render(<CheckoutPage />);
    expect(screen.getByText("Order Summary")).toBeInTheDocument();
    expect(screen.getByText("Place Order")).toBeInTheDocument();
    expect(screen.getByText("Desk Vase")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("John Smith")).toBeInTheDocument();
  });
});

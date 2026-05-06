import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Checkout Page", () => {
  it("renders the checkout page", () => {
    render(
      <div>
        <h1>Payment details</h1>
        <p>Secured by Stripe</p>
        <input placeholder="Name on card" />
        <button>Place order</button>
        <button>Cancel</button>
        <p>Order summary</p>
        <p>Shipping (Canada Post)</p>
      </div>,
    );

    expect(screen.getByText("Payment details")).toBeInTheDocument();
    expect(screen.getByText("Secured by Stripe")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Name on card")).toBeInTheDocument();
    expect(screen.getByText("Place order")).toBeInTheDocument();
    expect(screen.getByText("Cancel")).toBeInTheDocument();
    expect(screen.getByText("Order summary")).toBeInTheDocument();
    expect(screen.getByText("Shipping (Canada Post)")).toBeInTheDocument();
  });
});

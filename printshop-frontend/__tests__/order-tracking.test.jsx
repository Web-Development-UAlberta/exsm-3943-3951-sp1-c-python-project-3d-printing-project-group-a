import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import OrdersPage from "../app/orders/page";

describe("Order Tracking Page", () => {
  it("renders the order tracking page", () => {
    render(<OrdersPage />);
    expect(screen.getByText("Loading orders...")).toBeInTheDocument();
  });
});

import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import OrdersPage from "../app/orders/page";

describe("Order Tracking Page", () => {
  it("renders the order tracking page", () => {
    render(<OrdersPage />);
    expect(screen.getByText("My Orders")).toBeInTheDocument();
    expect(screen.getByText("Order History")).toBeInTheDocument();
    expect(screen.getAllByText("Pending").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Printing").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Shipped").length).toBeGreaterThan(0);
    expect(screen.getAllByText("Completed").length).toBeGreaterThan(0);
  });
});

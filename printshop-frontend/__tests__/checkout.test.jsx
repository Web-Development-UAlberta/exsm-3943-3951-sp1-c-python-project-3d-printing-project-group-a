import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import CheckoutPage from "../app/checkout/page";

jest.mock("next/navigation", () => ({
  useRouter: () => ({ push: jest.fn() }),
}));

describe("Checkout Page", () => {
  it("renders the checkout page", () => {
    render(<CheckoutPage />);
    expect(screen.getByText("Loading checkout...")).toBeInTheDocument();
  });
});

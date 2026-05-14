import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import RegisterPage from "../app/register/page";

describe("Register Page", () => {
  it("renders the register page", () => {
    render(<RegisterPage />);
    expect(screen.getByText("Create your account")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. Robel_M")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("e.g. Robel Measho"),
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. R@email.com")).toBeInTheDocument();
    expect(screen.getByText("Create my account")).toBeInTheDocument();
  });
});

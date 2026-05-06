import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Register Page", () => {
  it("renders the register page", () => {
    render(
      <div>
        <h1>Create your account</h1>
        <input placeholder="e.g. Roel_M" />
        <input placeholder="min 8 chars -- include a number and symbol" />
        <input placeholder="e.g. Robel Measho" />
        <input placeholder="e.g. R@email.com" />
        <input placeholder="e.g. 780-555-0101" />
        <input placeholder="e.g. Fox Creek" />
        <input placeholder="e.g. 123 Main St" />
        <input placeholder="e.g. AB" />
        <input placeholder="e.g. T5A 0A1" />
        <button>Create my account</button>
      </div>,
    );

    expect(screen.getByText("Create your account")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. Roel_M")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("e.g. Robel Measho"),
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. R@email.com")).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText("e.g. 780-555-0101"),
    ).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. Fox Creek")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. 123 Main St")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. AB")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. T5A 0A1")).toBeInTheDocument();
    expect(screen.getByText("Create my account")).toBeInTheDocument();
  });
});

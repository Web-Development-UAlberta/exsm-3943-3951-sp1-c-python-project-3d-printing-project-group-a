import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";

describe("Configurator Page", () => {
  it("renders the configurator page", () => {
    render(
      <div>
        <h1>Configurator</h1>
        <p>Model dimensions</p>
        <input placeholder="e.g. 100" />
        <button>Add to Cart</button>
        <p>Live price breakdown</p>
        <p>Shipping ( canada post )</p>
      </div>,
    );

    expect(screen.getByText("Configurator")).toBeInTheDocument();
    expect(screen.getByText("Model dimensions")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("e.g. 100")).toBeInTheDocument();
    expect(screen.getByText("Add to Cart")).toBeInTheDocument();
    expect(screen.getByText("Live price breakdown")).toBeInTheDocument();
    expect(screen.getByText("Shipping ( canada post )")).toBeInTheDocument();
  });
});

import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import ConfiguratorPage from "../app/product/[id]/page";

describe("Configurator Page", () => {
  it("renders the configurator page", () => {
    render(<ConfiguratorPage params={{ id: "1" }} />);
    expect(screen.getByText("Configurator")).toBeInTheDocument();
    expect(screen.getByText("Custom dimensions")).toBeInTheDocument();
    expect(screen.getByText("Add to Cart →")).toBeInTheDocument();
    expect(screen.getByText("Live price breakdown")).toBeInTheDocument();
  });
});

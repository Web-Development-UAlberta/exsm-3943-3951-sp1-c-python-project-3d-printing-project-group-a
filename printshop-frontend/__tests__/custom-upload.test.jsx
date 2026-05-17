import "@testing-library/jest-dom";
import { render, screen } from "@testing-library/react";
import ConfiguratorPage from "../app/product/[id]/page";

jest.mock("next/navigation", () => ({
  useParams: () => ({ id: "1" }),
  useRouter: () => ({ push: jest.fn() }),
}));

describe("Configurator Page", () => {
  it("renders the configurator page", () => {
    render(<ConfiguratorPage />);
    expect(screen.getByText("Loading model...")).toBeInTheDocument();
  });
});

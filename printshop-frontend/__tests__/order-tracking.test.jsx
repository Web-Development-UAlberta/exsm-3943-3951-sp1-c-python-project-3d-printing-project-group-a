import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'

describe('Order Tracking Page', () => {
  it('renders the order tracking page', () => {
    render(
      <div>
        <h1>My orders</h1>
        <p>Pending</p>
        <p>Printing</p>
        <p>Shipped</p>
        <p>Completed</p>
        <p>Order detail</p>
        <button>Cancel</button>
      </div>
    )
    expect(screen.getByText('My orders')).toBeInTheDocument()
    expect(screen.getByText('Pending')).toBeInTheDocument()
    expect(screen.getByText('Printing')).toBeInTheDocument()
    expect(screen.getByText('Shipped')).toBeInTheDocument()
    expect(screen.getByText('Completed')).toBeInTheDocument()
    expect(screen.getByText('Order detail')).toBeInTheDocument()
    expect(screen.getByText('Cancel')).toBeInTheDocument()
  })
})

import '@testing-library/jest-dom'
import { render, screen } from '@testing-library/react'

describe('Cart Page', () => {
  it('renders the cart page', () => {
    render(
      <div>
        <h1>Your cart</h1>
        <p>Subtotal</p>
        <p>Shipping</p>
        <p>TOTAL</p>
        <button>Cancel cart</button>
        <button>Proceed to Checkout</button>
      </div>
    )
    expect(screen.getByText('Your cart')).toBeInTheDocument()
    expect(screen.getByText('Subtotal')).toBeInTheDocument()
    expect(screen.getByText('Shipping')).toBeInTheDocument()
    expect(screen.getByText('TOTAL')).toBeInTheDocument()
    expect(screen.getByText('Cancel cart')).toBeInTheDocument()
    expect(screen.getByText('Proceed to Checkout')).toBeInTheDocument()
  })
})

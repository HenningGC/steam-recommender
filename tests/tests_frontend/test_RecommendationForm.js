// src/tests/test_RecommendationForm.js

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import RecommendationForm from '../RecommendationForm';

test('renders the form and allows user to input a value', () => {
  render(<RecommendationForm />);
  const inputElement = screen.getByPlaceholderText('Enter your input');
  fireEvent.change(inputElement, { target: { value: 'test input' } });
  expect(inputElement.value).toBe('test input');
});

test('submits the form and clears the input', async () => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      ok: true,
      json: () => Promise.resolve({ recommendations: ['Game 1', 'Game 2', 'Game 3'] }),
    })
  );

  render(<RecommendationForm />);
  const inputElement = screen.getByPlaceholderText('Enter your input');
  const submitButton = screen.getByText('Submit');

  fireEvent.change(inputElement, { target: { value: 'test input' } });
  fireEvent.click(submitButton);

  await waitFor(() => expect(inputElement.value).toBe(''));
});

const FAQS = [
  {
    id: "shipping-times",
    category: "Shipping",
    question: "How long does delivery take?",
    answer:
      "Standard delivery usually takes 3-7 business days. Express delivery is available for selected locations and typically arrives in 1-3 business days.",
    keywords: ["shipping", "delivery", "arrival", "express", "standard", "days"],
    actions: [
      "Ask for the delivery country before promising an exact ETA.",
      "Offer express shipping if the customer has a deadline.",
      "Send tracking instructions after the order ships.",
    ],
    handoff:
      "Customer is asking about delivery speed. Confirm country and order status before quoting an exact timeline.",
  },
  {
    id: "returns",
    category: "Returns",
    question: "Can I return an item?",
    answer:
      "Unused items can be returned within 30 days. The product should be in original condition with packaging included. Final-sale items are not eligible for return.",
    keywords: ["return", "refund", "exchange", "unused", "30 days", "final sale"],
    actions: [
      "Ask whether the item has been used.",
      "Confirm order date before approving the return window.",
      "Share the return instructions and expected refund timing.",
    ],
    handoff:
      "Customer is asking about returns. Check usage status, order date, and whether the item is final sale.",
  },
  {
    id: "size-guide",
    category: "Product",
    question: "How do I choose the right size?",
    answer:
      "Use the size chart on each product page and compare it with your actual measurements. If you are between two sizes, choose the larger size for a relaxed fit.",
    keywords: ["size", "fit", "measurement", "chart", "large", "small"],
    actions: [
      "Ask for the customer's measurements if needed.",
      "Share the product-specific size chart.",
      "Recommend the larger size when the customer is between sizes.",
    ],
    handoff:
      "Customer needs sizing help. Ask for measurements and compare them against the product-specific chart.",
  },
  {
    id: "bulk-orders",
    category: "Sales",
    question: "Do you support bulk orders?",
    answer:
      "Yes. Bulk orders are available for selected products. Please share the product name, quantity, delivery country, and target delivery date so the team can prepare a quote.",
    keywords: ["bulk", "wholesale", "quantity", "quote", "b2b", "large order"],
    actions: [
      "Ask for product name and quantity.",
      "Confirm delivery country and target date.",
      "Route the lead to sales for a custom quote.",
    ],
    handoff:
      "Potential bulk order. Collect product, quantity, country, and timeline before preparing a quote.",
  },
  {
    id: "appointment",
    category: "Booking",
    question: "How can I book an appointment?",
    answer:
      "You can book an appointment through the booking form or by sending your preferred date, time, service type, and contact details. The team will confirm availability.",
    keywords: ["appointment", "booking", "schedule", "service", "time", "date"],
    actions: [
      "Ask for preferred date and time.",
      "Confirm the service type.",
      "Collect phone or email for confirmation.",
    ],
    handoff:
      "Customer wants to book. Collect date, time, service type, and contact details.",
  },
  {
    id: "order-change",
    category: "Orders",
    question: "Can I change my order after purchase?",
    answer:
      "Order changes are possible before fulfillment begins. Please contact support as soon as possible with your order number and the change you need.",
    keywords: ["order", "change", "modify", "purchase", "fulfillment", "order number"],
    actions: [
      "Ask for the order number.",
      "Check whether fulfillment has started.",
      "Confirm the requested change in writing.",
    ],
    handoff:
      "Customer wants to modify an order. Verify order number and fulfillment status before confirming changes.",
  },
];

const stopWords = new Set(["the", "a", "an", "i", "do", "does", "can", "how", "is", "it", "to", "for", "of", "my", "after"]);

function tokenize(text) {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, " ")
    .split(/\s+/)
    .filter((word) => word && !stopWords.has(word));
}

function scoreFaq(query, faq) {
  const queryTokens = tokenize(query);
  const keywordText = faq.keywords.join(" ").toLowerCase();
  const questionText = faq.question.toLowerCase();
  const answerText = faq.answer.toLowerCase();

  let score = 0;
  for (const token of queryTokens) {
    if (keywordText.includes(token)) score += 22;
    if (questionText.includes(token)) score += 14;
    if (answerText.includes(token)) score += 6;
  }

  return Math.min(98, Math.max(12, score));
}

function findBestAnswer(query) {
  return FAQS.map((faq) => ({ ...faq, score: scoreFaq(query, faq) })).sort((a, b) => b.score - a.score)[0];
}

function renderAnswer(faq) {
  document.getElementById("answerTitle").textContent = `${faq.category} · ${faq.question}`;
  document.getElementById("answerText").textContent = faq.answer;
  document.getElementById("confidenceScore").textContent = `Match score: ${faq.score}%`;
  document.getElementById("categoryPill").textContent = faq.category;
  document.getElementById("handoffNote").textContent = faq.handoff;

  const list = document.getElementById("nextActions");
  list.innerHTML = "";
  for (const action of faq.actions) {
    const item = document.createElement("li");
    item.textContent = action;
    list.appendChild(item);
  }
}

function ask() {
  const input = document.getElementById("questionInput");
  renderAnswer(findBestAnswer(input.value));
}

document.getElementById("askButton").addEventListener("click", ask);
document.getElementById("questionInput").addEventListener("keydown", (event) => {
  if (event.key === "Enter") ask();
});

for (const button of document.querySelectorAll("[data-question]")) {
  button.addEventListener("click", () => {
    document.getElementById("questionInput").value = button.dataset.question;
    ask();
  });
}

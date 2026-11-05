const dbRef = db.getSiblingDB('vulnshop');

if (!dbRef.getCollectionNames().includes('reviews')) {
  dbRef.createCollection('reviews');
}
if (!dbRef.getCollectionNames().includes('catalog')) {
  dbRef.createCollection('catalog');
}

dbRef.reviews.updateOne(
  { _id: 'review-lab-1' },
  { $setOnInsert: { product_id: 1, user_id: 2, rating: 5, text: 'Synthetic training review', created_at: new Date() } },
  { upsert: true }
);

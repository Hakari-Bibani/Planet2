import React, { useState, useEffect } from 'react';

// Mock data service (replace with actual API/database calls)
const mockDataService = {
  getTreeNames: async () => [
    "Oak", "Maple", "Pine", "Birch", "Elm"
  ],
  
  getPackagingTypes: async () => [
    "Bare Root", "Container", "Balled and Burlapped"
  ],
  
  getHeightRange: async (treeName) => {
    // Simulated height range based on tree name
    const heightRanges = {
      "Oak": { min: 10, max: 80 },
      "Maple": { min: 15, max: 70 },
      "Pine": { min: 20, max: 90 },
      "Birch": { min: 10, max: 60 },
      "Elm": { min: 25, max: 75 }
    };
    return heightRanges[treeName] || { min: 0, max: 100 };
  },
  
  searchInventory: async (params) => {
    // Simulated search results
    return [
      {
        quantityInStock: 50,
        price: 49.99,
        growthRate: "Moderate",
        scientificName: "Quercus rubra",
        shape: "Rounded",
        wateringDemand: "Moderate",
        origin: "North America",
        soilType: "Well-drained",
        rootType: "Deep",
        leafType: "Deciduous",
        address: "123 Nursery Lane"
      }
    ];
  }
};

export default function TreeInventorySearch() {
  // State management
  const [treeNames, setTreeNames] = useState([]);
  const [packagingTypes, setPackagingTypes] = useState([]);
  const [selectedTree, setSelectedTree] = useState(null);
  const [selectedPackaging, setSelectedPackaging] = useState(null);
  const [heightRange, setHeightRange] = useState({ min: 0, max: 100 });
  const [selectedHeight, setSelectedHeight] = useState([0, 100]);
  const [searchResults, setSearchResults] = useState([]);

  // Fetch initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      const trees = await mockDataService.getTreeNames();
      const packages = await mockDataService.getPackagingTypes();
      setTreeNames(trees);
      setPackagingTypes(packages);
    };
    fetchInitialData();
  }, []);

  // Update height range when tree changes
  useEffect(() => {
    const fetchHeightRange = async () => {
      if (selectedTree) {
        const range = await mockDataService.getHeightRange(selectedTree);
        setHeightRange(range);
        setSelectedHeight([range.min, range.max]);
      }
    };
    fetchHeightRange();
  }, [selectedTree]);

  // Search handler
  const handleSearch = async () => {
    const results = await mockDataService.searchInventory({
      treeName: selectedTree,
      packagingType: selectedPackaging,
      minHeight: selectedHeight[0],
      maxHeight: selectedHeight[1]
    });
    setSearchResults(results);
  };

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-6 text-primary">
        Tree Inventory Search
      </h1>

      <div className="bg-white shadow-md rounded-lg mb-6 p-6">
        <h2 className="text-xl font-semibold mb-4">Search Filters</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {/* Tree Name Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Tree Name
            </label>
            <select 
              className="w-full p-2 border rounded-md"
              onChange={(e) => setSelectedTree(e.target.value)}
              value={selectedTree || ''}
            >
              <option value="">Choose a Tree</option>
              {treeNames.map(name => (
                <option key={name} value={name}>
                  {name}
                </option>
              ))}
            </select>
          </div>

          {/* Packaging Type Selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Packaging Type
            </label>
            <select 
              className="w-full p-2 border rounded-md"
              onChange={(e) => setSelectedPackaging(e.target.value)}
              value={selectedPackaging || ''}
            >
              <option value="">Choose Packaging</option>
              {packagingTypes.map(type => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Height Range Slider */}
        {selectedTree && (
          <div className="mt-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Height Range (feet)
            </label>
            <div className="flex items-center space-x-4">
              <span className="text-sm w-12 text-right">{selectedHeight[0]} ft</span>
              <input 
                type="range"
                min={heightRange.min}
                max={heightRange.max}
                value={selectedHeight[0]}
                onChange={(e) => setSelectedHeight([Number(e.target.value), selectedHeight[1]])}
                className="flex-grow"
              />
              <input 
                type="range"
                min={heightRange.min}
                max={heightRange.max}
                value={selectedHeight[1]}
                onChange={(e) => setSelectedHeight([selectedHeight[0], Number(e.target.value)])}
                className="flex-grow"
              />
              <span className="text-sm w-12">{selectedHeight[1]} ft</span>
            </div>
          </div>
        )}

        {/* Search Button */}
        <button 
          onClick={handleSearch} 
          className="w-full mt-4 p-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          disabled={!selectedTree}
        >
          Search Inventory
        </button>
      </div>

      {/* Search Results */}
      {searchResults.length > 0 && (
        <div className="bg-white shadow-md rounded-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Search Results</h2>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse">
              <thead>
                <tr className="bg-gray-100">
                  <th className="border p-2 text-left">Quantity</th>
                  <th className="border p-2 text-left">Price</th>
                  <th className="border p-2 text-left">Growth Rate</th>
                  <th className="border p-2 text-left">Scientific Name</th>
                  <th className="border p-2 text-left">Origin</th>
                  <th className="border p-2 text-left">Soil Type</th>
                </tr>
              </thead>
              <tbody>
                {searchResults.map((result, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="border p-2">{result.quantityInStock}</td>
                    <td className="border p-2">${result.price.toFixed(2)}</td>
                    <td className="border p-2">{result.growthRate}</td>
                    <td className="border p-2">{result.scientificName}</td>
                    <td className="border p-2">{result.origin}</td>
                    <td className="border p-2">{result.soilType}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

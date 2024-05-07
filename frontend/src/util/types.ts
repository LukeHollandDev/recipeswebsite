export type User = {
  id: number;
  username: string;
  email: string;
  access_token: string;
};

export type Recipe = {
  id: number;
  id_other: string;
  title: string;
  description: string;
  url: string;
  image: string | null;
  cuisine: string | null;
  prepTime: number | null;
  totalTime: number | null;
  servings: number | null;
};

export type Nutriant = {
  recipe_id: number;
  amount: number;
  name: string;
  unit: string;
  id: number;
};

export type Resource = {
  type: string;
  name: string;
  id: number;
  recipe_id: number;
  value: string;
};

export type Ingredient = {
  id: number;
  note: string | null;
  amount_upper: number;
  amount_lower: number;
  name: string;
  unit: string | null;
  group_id: number;
};

export type IngredientGroup = {
  name: string | null;
  id: number;
  recipe_id: number;
  ingredients: Ingredient[];
};

export type Instruction = {
  image: string;
  text: string;
  index: number;
  group_id: number;
  id: number;
};

export type InstructionGroup = {
  name: string | null;
  id: number;
  recipe_id: number;
  instructions: Instruction[];
};

export type RecipeFull = Recipe & {
  nutrients: Nutriant[];
  resources: Resource[];
  ingredient_groups: IngredientGroup[];
  instruction_groups: InstructionGroup[];
};

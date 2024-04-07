import pandas as pd
import sqlalchemy
import os
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import StratifiedKFold, cross_validate

# Шаг 1: Получение данных
load_dotenv()
host = os.environ.get('DB_DESTINATION_HOST')
port = os.environ.get('DB_DESTINATION_PORT')
db = os.environ.get('DB_DESTINATION_NAME')
username = os.environ.get('DB_DESTINATION_USER')
password = os.environ.get('DB_DESTINATION_PASSWORD')
dst_conn = create_engine(f'postgresql://{dst_username}:{dst_password}@{dst_host}:{dst_port}/{dst_db}', connect_args={'sslmode':'require'})

data = pd.read_sql('select * from clean_users_churn', dst_conn, index_col='customer_id')

# Шаг 2: Преобработка данных и обучение модели
cat_features = data.select_dtypes(include='object')
potential_binary_features = cat_features.nunique() == 2
binary_cat_features = cat_features[potential_binary_features[potential_binary_features].index]
other_cat_features = cat_features[potential_binary_features[~potential_binary_features].index]
num_features = data.select_dtypes(['float'])

preprocessor = ColumnTransformer(
    [
    ('binary', OneHotEncoder(drop='if_binary'), binary_cat_features.columns.tolist()),
    ('cat', CatBoostEncoder(), other_cat_features.columns.tolist()),
    ('num', StandardScaler(), num_features.columns.tolist())
    ],
    remainder='drop',
    verbose_feature_names_out=False
)

model = CatBoostClassifier(auto_class_weights='Balanced')

pipeline = Pipeline(
    [
        ('preprocessor', preprocessor),
        ('model', model)
    ]
)
pipeline.fit(data, data['target'])

# Шаг 3: Проверка качества на кросс-валидации
cv_strategy = StratifiedKFold(n_splits=5)
cv_res = cross_validate(
    pipeline,
    data,
    data['target'],
    cv=cv_strategy,
    n_jobs=-1,
    scoring=['f1', 'roc_auc']
    )
for key, value in cv_res.items():
    cv_res[key] = round(value.mean(), 3)
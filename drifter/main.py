import io

import numpy as np
import pandas as pd

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

import settings

def get_dataset(drift_prob: float, rows: int, cols: int) -> pd.DataFrame:
  
  def _get_loc():
    return 0 if np.random.random() > drift_prob else np.random.random()
  
  return pd.DataFrame(
    np.column_stack([
      np.random.normal(loc=_get_loc(), size=rows) for _ in range(cols)
    ]),
    columns=[f'feat{i}' for i in range(cols)]
  )


api_prefix = '/api/v1'
cfg = settings.Config()
app = FastAPI()


@app.get(f'{api_prefix}/data')
def data():
  df = get_dataset(
    cfg.drift_prob, 
    cfg.drift_rows, 
    cfg.drift_cols
  )
    
  response = StreamingResponse(
    io.StringIO(df.to_csv(index=False)),
    headers={
      'Content-Disposition': 'attachment; filename=dataset.csv',
    },
    media_type='text/csv'
  )

  return response


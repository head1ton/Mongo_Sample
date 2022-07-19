import pydantic


class BaseModel(pydantic.BaseModel):

    @pydantic.root_validator(pre=True)
    def _min_properties(cls, data):
        if not data:
            raise ValueError("At least one property is required")
        return data

    def dict(self, include_nulls=False, **kwargs):
        kwargs["exclude_none"] = not include_nulls
        return super().dict(**kwargs)

    class Config:
        extra = pydantic.Extra.forbid
        anystr_strip_whitespace = True

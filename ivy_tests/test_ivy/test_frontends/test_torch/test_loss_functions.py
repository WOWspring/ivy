# global
from hypothesis import given, strategies as st

# local
import ivy_tests.test_ivy.helpers as helpers
from ivy_tests.test_ivy.helpers import handle_cmd_line_args


# cross_entropy
@handle_cmd_line_args
@given(
    dtype_and_input=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        allow_inf=False,
        min_num_dims=2,
        max_num_dims=2,
        min_dim_size=1,
    ),
    dtype_and_target=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0.0,
        max_value=1.0,
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_weights=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    size_average=st.booleans(),
    reduce=st.booleans(),
    reduction=st.sampled_from(["mean", "none", "sum"]),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.cross_entropy"
    ),
    label_smoothing=helpers.floats(min_value=0, max_value=0.49),
)
def test_torch_cross_entropy(
    dtype_and_input,
    dtype_and_target,
    dtype_and_weights,
    size_average,
    reduce,
    reduction,
    label_smoothing,
    as_variable,
    num_positional_args,
    native_array,
):
    inputs_dtype, input = dtype_and_input
    target_dtype, target = dtype_and_target
    weights_dtype, weights = dtype_and_weights
    helpers.test_frontend_function(
        input_dtypes=inputs_dtype + target_dtype + weights_dtype,
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend="torch",
        fn_tree="nn.functional.cross_entropy",
        input=input[0],
        target=target[0],
        weight=weights[0].reshape(-1),
        size_average=size_average,
        reduce=reduce,
        reduction=reduction,
        label_smoothing=label_smoothing,
    )


# binary_cross_entropy
@handle_cmd_line_args
@given(
    dtype_and_true=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0.0,
        max_value=1.0,
        large_abs_safety_factor=2,
        small_abs_safety_factor=2,
        safety_factor_scale="linear",
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_pred=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=1.0013580322265625e-05,
        max_value=1.0,
        large_abs_safety_factor=2,
        small_abs_safety_factor=2,
        safety_factor_scale="linear",
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_weight=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=1.0013580322265625e-05,
        max_value=1.0,
        allow_inf=False,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    size_average=st.booleans(),
    reduce=st.booleans(),
    reduction=st.sampled_from(["mean", "none", "sum", None]),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.binary_cross_entropy"
    ),
)

def test_torch_binary_cross_entropy(
    dtype_and_true,
    dtype_and_pred,
    dtype_and_weight,
    size_average,
    reduce,
    reduction,
    as_variable,
    num_positional_args,
    native_array,
):
    pred_dtype, pred = dtype_and_pred
    true_dtype, true = dtype_and_true
    weight_dtype, weight = dtype_and_weight
    helpers.test_frontend_function(
        input_dtypes=[pred_dtype, true_dtype, weight_dtype],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        frontend="torch",
        fn_tree="nn.functional.binary_cross_entropy",
        input=pred[0],
        target=true[0],
        weight=weight[0],
        size_average=size_average,
        reduce=reduce,
        reduction=reduction,
    )


# smooth_l1_loss
@given(
    dtype_and_true=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=0.0,
        max_value=1.0,
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    dtype_and_pred=helpers.dtype_and_values(
        available_dtypes=helpers.get_dtypes("float"),
        min_value=1.0013580322265625e-05,
        max_value=1.0,
        allow_inf=False,
        exclude_min=True,
        exclude_max=True,
        min_num_dims=1,
        max_num_dims=1,
        min_dim_size=2,
    ),
    reduction=st.sampled_from(["mean", "none", "sum"]),
    beta=helpers.floats(
        min_value=1.0013580322265625e-05,
        allow_inf=False,
        allow_nan=False,
        exclude_min=True,
        exclude_max=True,
    ),
    as_variable=helpers.list_of_length(x=st.booleans(), length=2),
    num_positional_args=helpers.num_positional_args(
        fn_name="ivy.functional.frontends.torch.smooth_l1_loss"
    ),
    native_array=helpers.list_of_length(x=st.booleans(), length=2),
)
def test_smooth_l1_loss(
        dtype_and_true,
        dtype_and_pred,
        reduction,
        beta,
        as_variable,
        num_positional_args,
        native_array,
        fw,
):
    pred_dtype, pred = dtype_and_pred
    true_dtype, true = dtype_and_true
    beta = beta

    helpers.test_frontend_function(
        input_dtypes=[pred_dtype, true_dtype],
        as_variable_flags=as_variable,
        with_out=False,
        num_positional_args=num_positional_args,
        native_array_flags=native_array,
        fw=fw,
        frontend="torch",
        fn_tree="nn.functional.smooth_l1_loss",
        input=pred[0],
        target=true[0],
        reduction=reduction,
        beta=beta,
    )

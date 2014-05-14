module Dydx
  module Algebra
    class Formula
      include Helper
      attr_accessor :f, :g, :operator

      def initialize(f, g, operator)
        @f, @g, @operator = f, g, operator
      end

      def differentiate(sym=:x)
        case @operator
        when :+
          f.d(sym) + g.d(sym)
        when :-
          f.d(sym) - g.d(sym)
        when :*
          (f.d(sym) * g) + (f * g.d(sym))
        when :/
          ((f.d(sym) * g) - (f * g.d(sym)))/(g ^ _(2))
        when :^
          # TODO:
          if f == sym
            g * (f ^ (g - 1))
          else
            self * (g * log(f)).d(sym)
          end
        end
      end
      alias_method :d, :differentiate

      def to_s
        if (subtraction? && f.is_0?) ||
          (multiplication? && (f.is_minus1? || g.is_minus1?)  )
          "( - #{g.to_s} )"
        else
          "( #{f.to_s} #{@operator} #{g.to_s} )"
        end
      end

      def include?(x)
        f == x || g == x
      end

      def openable?(x)
        if x.is_a?(Num) || x.is_a?(Fixnum)
          f.class == x.class || g.class == x.class
        else
          false
        end
      end
    end
  end
end